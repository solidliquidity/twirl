from datetime import timedelta

import twirl

twirl.manifest(
    twirl.Table(
        job=twirl.PythonJob(update_method=twirl.UpdateMethod.REPLACE),
        # consider using twirl.TriggerWithoutInputs(once_every=timedelta(hours=X)) if this data is updated frequently
        trigger_conditions=twirl.TriggerAt(cron_string="0 0 * * *"),
    )
)
