-- ￼When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

SELECT r.rewardsReceiptStatus, SUM(r.purchasedItemCount) AS totalItems
FROM receipts r 
RIGHT JOIN ItemList i ON r.receiptId = i.receiptId
WHERE r.rewardsReceiptStatus = 'FINISHED' OR r.rewardsReceiptStatus = 'RejecREJECTEDted'
GROUP BY r.rewardsReceiptStatus
ORDER BY totalItems DESC