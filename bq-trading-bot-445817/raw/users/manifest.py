import twirl

twirl.manifest(
    twirl.Table(
        schema=twirl.Schema(
            [
                twirl.Column("user_id", twirl.String(), is_primary_key=True),
                twirl.Column("created_at", twirl.String(), is_event_time=True),
                twirl.Column("status", twirl.String()),
            ]
        ),
        job=twirl.LoadStaticFiles(
            twirl.UpdateMethod.REPLACE,
            data_file_names=["users.csv"],
            read_as_strings=True,
            add_source_file_column=False,
        ),
        trigger_conditions=twirl.Static(),
        tags=["cash_flow_prediction"],
    )
)
