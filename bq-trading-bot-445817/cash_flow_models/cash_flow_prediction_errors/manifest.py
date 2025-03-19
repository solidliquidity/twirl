import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("date", twirl.Date()),
                twirl.Column("user_id", twirl.String()),
                twirl.Column("absolute_error", twirl.Float64()),
            ]
        ),
        inputs=[
            twirl.Input(
                "bq-trading-bot-445817/cash_flow_models/cash_flow_prediction_estimates"
            ),
            twirl.Input("bq-trading-bot-445817/aggregates/daily_transactions"),
        ],
        job=twirl.PythonJob(twirl.UpdateMethod.REPLACE),
        tags=["cash_flow_prediction"],
    )
)
