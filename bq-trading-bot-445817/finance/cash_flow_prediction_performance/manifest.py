import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("month", twirl.Date()),
                twirl.Column("mean_absolute_error", twirl.Float64()),
            ]
        ),
        inputs=[
            twirl.Input(
                "bq-trading-bot-445817/cash_flow_models/cash_flow_prediction_errors"
            )
        ],
        job=twirl.BigQueryJob(twirl.UpdateMethod.REPLACE),
        tags=["cash_flow_prediction"],
    )
)
