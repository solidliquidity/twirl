import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("date", twirl.Date()),
                twirl.Column("user_id", twirl.String()),
                twirl.Column("estimated_daily_cash_flow", twirl.Float64()),
                twirl.Column("prediction_horizon_days", twirl.Integer()),
                twirl.Column("estimated_total_cash_flow", twirl.Float64()),
            ]
        ),
        inputs=[
            twirl.Input(
                "bq-trading-bot-445817/cash_flow_models/cash_flow_prediction_features"
            )
        ],
        job=twirl.PythonJob(twirl.UpdateMethod.REPLACE),
        tags=["cash_flow_prediction"],
    )
)
