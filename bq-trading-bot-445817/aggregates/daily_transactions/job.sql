with all_dates as (
    select
        dates as date,
        user_id
    from
        unnest(
            generate_date_array('2022-01-01', current_date, interval 1 day)
        ) as dates
    cross join (select distinct user_id from `trading-bot-445817.clean.users`)
)

select
    d.date,
    d.user_id,
    count(t.amount_eur) as n_transactions,
    coalesce(sum(t.amount_eur), 0) as total_amount_eur
from all_dates as d
left join `trading-bot-445817.clean.transactions` as t
    on d.date = extract(date from t.created_at)
        and d.user_id = t.user_id
group by
    d.date,
    d.user_id
order by
    d.date desc,
    d.user_id asc
