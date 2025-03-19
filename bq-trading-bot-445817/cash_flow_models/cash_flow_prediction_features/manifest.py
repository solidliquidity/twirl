import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("date", twirl.Date()),
                twirl.Column("user_id", twirl.String()),
                twirl.Column("total_amount_eur_last_30_days", twirl.Float64()),
            ]
        ),
        inputs=[twirl.Input("bq-trading-bot-445817/aggregates/daily_transactions")],
        job=twirl.BigQueryJob(twirl.UpdateMethod.REPLACE),
        tags=["cash_flow_prediction"],
    )
)
