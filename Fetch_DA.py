#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
from datetime import datetime
import unicodedata
import matplotlib.pyplot as plt
import seaborn as sns


# # Step1 Data importing and Normalization

# In[2]:


brands = pd.read_json('brands.json', lines=True)
users = pd.read_json('users.json', lines=True)
receipts = pd.read_json('receipts.json', lines=True)


# In[3]:


brands['_id']
# users['_id']
# receipts['_id']


# In[4]:


brands['_id'] = brands['_id'].apply(lambda x: list(x.values())[0])
users['_id'] = users['_id'].apply(lambda x: list(x.values())[0])
receipts['_id'] = receipts['_id'].apply(lambda x: list(x.values())[0])
brands = brands.rename(columns = {'_id':'brandsId'})
users = users.rename(columns = {'_id':'userId'})
receipts = receipts.rename(columns = {'_id':'receiptsId'})


# In[5]:


brands.head()


# In[6]:


def to_date(x):
    if type(x) == float:
        pass
    else:
        return(pd.to_datetime(list(x.values())[0], unit = 'ms'))


# In[7]:


users['createdDate'] = users['createdDate'].apply(lambda x:to_date(x))
users['lastLogin'] = users['lastLogin'].apply(lambda x:to_date(x))


# In[8]:


users.head()


# In[9]:


receipts['createDate'] = receipts['createDate'].apply(lambda x:to_date(x))
receipts['dateScanned'] = receipts['dateScanned'].apply(lambda x:to_date(x))
receipts['finishedDate'] = receipts['finishedDate'].apply(lambda x:to_date(x))
receipts['modifyDate'] = receipts['modifyDate'].apply(lambda x:to_date(x))
receipts['pointsAwardedDate'] = receipts['pointsAwardedDate'].apply(lambda x:to_date(x))
receipts['purchaseDate'] = receipts['purchaseDate'].apply(lambda x:to_date(x))


# In[10]:


receipts.head()


# In[11]:


receipts['rewardsReceiptItemList']
#need to create an Itemlist to store the information for rewardsReceiptItemList


# In[12]:


def expand(df, col):
    df[col] = df[col].apply(lambda x : [x] if not isinstance(x, list) else x)
    return df.drop(col, axis = 1).join(pd.DataFrame(list(df[col])).stack().reset_index(level = 1, drop = True).rename(col))

def Dic_expand(x, key):
    if type(x) == dict and key in x.keys():
        return x[key]


# In[13]:


ItemList = receipts[['rewardsReceiptItemList','receiptsId','userId']].copy()
ItemList = expand(ItemList, 'rewardsReceiptItemList').reset_index()
ItemList = ItemList.rename(columns = {'index':'originalId'})


# In[14]:


ItemList


# In[15]:


cols = []
for i in ItemList['rewardsReceiptItemList']:
    if type(i) != float:
        for j in i.keys():
            if j not in cols:
                cols.append(j)


# In[16]:


cols


# In[17]:


Itemlist = pd.DataFrame(columns = cols)

for i in range(len(cols)):
    col = Itemlist.columns[i]
    Itemlist[col] = ItemList['rewardsReceiptItemList'].apply(lambda x: Dic_expand(x,col))


# In[18]:


ItemList = pd.concat([ItemList, Itemlist], axis = 1)
ItemList.drop(['rewardsReceiptItemList'], axis = 1, inplace = True)


# In[19]:


ItemList.head()


# In[20]:


receipts.drop(['rewardsReceiptItemList'], axis = 1, inplace = True)
brands.drop(['cpg'], axis = 1, inplace = True)


# In[21]:


brands.head(2)


# In[22]:


users.head(2)


# In[23]:


receipts.head(2)


# In[24]:


ItemList.head(2)


# In[25]:


brands.to_csv("brands.csv", encoding = 'utf-8')
receipts.to_csv("receipts.csv", encoding = 'utf-8')
users.to_csv("users.csv", encoding = 'utf-8')
ItemList.to_csv("ItemList.csv", encoding = 'utf-8')


# # Checking data quality and EDA

# In[26]:


brands.info()


# In[27]:


ItemList.info()


# In[57]:


users.info()


# In[58]:


receipts.info()


# ## 1. Check missing value

# In[59]:


receipts.isnull().sum()


# In[61]:


brands.isnull().sum()


# In[62]:


users.isnull().sum()


# In[60]:


ItemList.isnull().sum()


# ## 2. Check duplicated value

# In[63]:


receipts.duplicated().value_counts()


# In[64]:


users.duplicated().value_counts()


# In[65]:


brands.duplicated().value_counts()


# In[66]:


ItemList.duplicated().value_counts()


# ## 3.  Check the relationship of barcode between ItemList and brands table

# In[28]:


brands['barcode']


# In[29]:


brands['barcode'] = brands['barcode'].astype(str)


# In[30]:


ItemList['barcode']


# In[31]:


Item_null = ItemList['barcode'].isnull().sum()
Item_sum = len(ItemList)

null_persent = round(100*(Item_null / Item_sum),2)
null_persent


# The total missing part of ItemListss barcode reaches 58.14%, which is more than half of the entire data.  The data quality is relatively low with ItemLists' barcode.
# Then I'll go checking the unique data of barcode

# In[32]:


len(ItemList['barcode'].unique())


# In[33]:


len(brands['barcode'].unique())


# In[34]:


ItemList['barcode'].describe()


# In[35]:


brands['barcode'].describe()


# In[36]:


#Inner join two lists on 'barcode' to show the shared barcode between ItemList and brands
share_barcode = len(pd.merge(left = ItemList, right = brands,how = 'inner', on = ['barcode']))
share_barcode


# In[37]:


share_persent = round(100*(share_barcode / len(ItemList['barcode'].unique())),2)
share_persent


# There are only 15.64% of barcode in ItemList can be found in brands' barcode, and also the entire barcode in ItemList is not uniform, some with 4 digits and some are combined with number and string, the entire data quality of barcode in ItemList is very low.

# ## 4. Check the relationship of userId between Users and Receipts table

# In[49]:


# share_userid = len(pd.merge(left = receipts, right = users,how = 'inner', on = ['userId']))
# share_userid


# In[55]:


#This function returns the userId that connot be found in receipts table
def missing_uid():
    ruid = receipts['userId'].unique()
    uid = users['userId'].unique()
    missing_uid = []
    for i in ruid:
        if i not in uid:
            missing_uid.append(i)
    
    return len(missing_uid)


# In[56]:


missing_uid()


# There are 117 records of userId in receipts cannot be found in users' userId

# ## Check possible outliers

# In[67]:


boxplot = receipts.boxplot(column=['bonusPointsEarned', 'pointsEarned'])

