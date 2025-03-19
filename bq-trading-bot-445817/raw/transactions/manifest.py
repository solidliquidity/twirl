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
                twirl.Column("amount_eur_cents", twirl.Integer()),
            ]
        ),
        job=twirl.PythonJob(twirl.UpdateMethod.APPEND),
        trigger_conditions=twirl.TriggerWithoutInputs(once_every=timedelta(hours=24)),
        tags=["cash_flow_prediction"],
    )
)
