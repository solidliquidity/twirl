import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("user_id", twirl.String(), is_primary_key=True),
                twirl.Column("status", twirl.String()),
            ]
        ),
        inputs=[twirl.Input("bq-trading-bot-445817/raw/users")],
        job=twirl.BigQueryJob(twirl.UpdateMethod.REPLACE),
        trigger_conditions=twirl.TriggerAt(cron_string="0 0 * * *"),
        tags=["cash_flow_prediction"],
    )
)
