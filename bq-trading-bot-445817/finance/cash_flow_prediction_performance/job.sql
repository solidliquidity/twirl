select
    date_trunc(date, month) as month,
    avg(absolute_error) as mean_absolute_error
from `trading-bot-445817.cash_flow_models.cash_flow_prediction_errors`
group by
    month
order by
    month desc
