import pandas as pd

from . import util


def job(input_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    estimates = input_tables[
        "bq-trading-bot-445817/cash_flow_models/cash_flow_prediction_estimates"
    ]
    actuals = input_tables["bq-trading-bot-445817/aggregates/daily_transactions"]

    df = util.merge(actuals, estimates, ["date", "user_id"])
    df["absolute_error"] = df["total_amount_eur"] - df["estimated_daily_cash_flow"]

    return df[["date", "user_id", "absolute_error"]]
