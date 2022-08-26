SELECT name_pr,	town, phone_num, contract_id, date_c
FROM provider
where 1
    and (to_days(current_date) - to_days(date_c)) < '$days_num'