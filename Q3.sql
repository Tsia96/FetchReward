-- ￼When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

SELECT AVG(totalSpent) AS averageSpent
FROM receipts
WHERE rewardsReceiptStatus = 'FINISHED' OR rewardsReceiptStatus = 'RejecREJECTEDted'
GROUP BY rewardsReceiptStatus
ORDER BY averageSpent DESC

