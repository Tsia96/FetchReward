-- What are the top 5 brands by receipts scanned for most recent month?

SELECT b.name
FROM receipts r 
RIGHT JOIN ItemsList i ON r.receiptId = i.receiptId 
LEFT JOIN brands b ON b.barcode = i.barcode
WHERE DATE_FORMAT(FROM_UNIXTIME(r.dataScanned), '%Y%m') = DATE_FORMAT(CURDATE(), '%Y%m') 
GROUP BY b.brandId 
ORDER BY count(*) DESC
LIMIT 5