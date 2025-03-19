from datetime import timedelta

import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("transaction_id", twirl.String(), is_primary_key=True),
                twirl.Column("user_id", twirl.String()),
                twirl.Column(
                    "created_at",
                    twirl.Timestamp(unit="us", tz="UTC"),
                    is_event_time=True,
                ),
                twirl.Column("amount_eur", twirl.Float64()),
            ]
        ),
        inputs=[
            twirl.Input(
                "bq-trading-bot-445817/raw/transactions",
                incremental=twirl.OnlyNewerRows(
                    output_time="created_at",
                    input_time="created_at",
                    lookback_interval=timedelta(hours=24),
                    output_unique_id="transaction_id",
                    input_unique_id="transaction_id",
                ),
            )
        ],
        job=twirl.BigQueryJob(twirl.UpdateMethod.REPLACE),
        tags=["cash_flow_prediction"],
    )
)
