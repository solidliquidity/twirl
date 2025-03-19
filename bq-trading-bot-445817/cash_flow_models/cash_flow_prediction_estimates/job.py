import pandas as pd

PREDICTION_HORIZON_DAYS = 360


def job(input_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    df = input_tables["bq-trading-bot-445817/cash_flow_models/cash_flow_prediction_features"]

    df["estimated_daily_cash_flow"] = df["total_amount_eur_last_30_days"] / 30
    df["prediction_horizon_days"] = PREDICTION_HORIZON_DAYS
    df["estimated_total_cash_flow"] = (
        df["estimated_daily_cash_flow"] * PREDICTION_HORIZON_DAYS
    )

    return df[
        [
            "date",
            "user_id",
            "estimated_daily_cash_flow",
            "prediction_horizon_days",
            "estimated_total_cash_flow",
        ]
    ]
