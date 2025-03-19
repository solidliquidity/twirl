select
    transaction_id,
    user_id,
    created_at,
    amount_eur_cents / 100.0 as amount_eur
from `trading-bot-445817.raw.transactions`
order by created_at
