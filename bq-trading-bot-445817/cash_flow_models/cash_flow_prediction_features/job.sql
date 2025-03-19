select
    date,
    user_id,
    sum(total_amount_eur) over (
        partition by user_id
        order by date asc rows between 29 preceding and current row
    ) as total_amount_eur_last_30_days
from `trading-bot-445817.aggregates.daily_transactions`
order by
    date desc,
    user_id asc
