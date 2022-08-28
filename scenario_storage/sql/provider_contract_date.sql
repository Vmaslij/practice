SELECT name_pr,	town, phone_num, contract_id, date_c
FROM provider
WHERE 1
and month(date_c) = '$month_c' and year(date_c) = '$year_c'