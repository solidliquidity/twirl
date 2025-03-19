from datetime import timedelta

import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("date", twirl.Date(), is_primary_key=True),
                twirl.Column("user_id", twirl.String(), is_primary_key=True),
                twirl.Column("n_transactions", twirl.Integer()),
                twirl.Column("total_amount_eur", twirl.Float64()),
            ]
        ),
        inputs=[
            twirl.Input(
                "bq-trading-bot-445817/clean/transactions",
            ),
            twirl.Input("bq-trading-bot-445817/clean/users"),
        ],
        job=twirl.BigQueryJob(twirl.UpdateMethod.REPLACE),
        tags=["cash_flow_prediction"],
    )
)
