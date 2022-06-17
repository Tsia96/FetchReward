-- ￼How does the ranking of the top 5 brands by receipts scanned for the recent month compare to the ranking for the previous month?

CREATE VIEW [top5_bands_recent_month] AS:
SELECT b.name
FROM receipts r 
RIGHT JOIN ItemsList i ON r.receiptId = i.receiptId 
LEFT JOIN brands b ON b.barcode = i.barcode
WHERE DATE_FORMAT(FROM_UNIXTIME(r.dataScanned), '%Y%m') = DATE_FORMAT(CURDATE(), '%Y%m') 
GROUP BY b.brandId 
ORDER BY count(*) DESC
LIMIT 5

create VIEW [top5_bands_last_month] AS:
SELECT b.name
FROM receipts r 
RIGHT JOIN ItemsList i ON r.receiptId = i.receiptId 
LEFT JOIN brands b ON b.barcode = i.barcode
WHERE PERIOD_DIFF(DATE_FORMAT(NOW() , '%Y%m'), date_format(`add_time`, '%Y%m')) =1
GROUP BY b.brandId 
ORDER BY count(*) DESC
LIMIT 5

select * from top5_bands_recent_month;
select * from top5_bands_last_month;
