import twirl

twirl.project_config(
    project_name="my-project",
    secrets=[twirl.EnvironmentSecrets()],
    datastores=[
        twirl.BigQueryDatastore(
            name="bq-trading-bot-445817",
            gcp_project_id="trading-bot-445817",
            gcp_location="europe-west2",
        ),
        # Example of a second Snowflake datastore, with a separate dev datastore
        # twirl.BigQueryDatastore(
        #     name="prod-db,
        #     gcp_project_id="trading-bot-445817",
        #     gcp_location="europe-west2",
        #     dev_datastore="dev-db",
        # ),
        # twirl.BigQueryDatastore(
        #     name="dev-db",
        #     gcp_project_id="trading-bot-445817",
        #     gcp_location="europe-west2",
        # ),
    ],
    container_registry=twirl.GcpContainerRegistry(
        gcp_region="europe-west2",
        registry_host="europe-west2-docker.pkg.dev",
        gcp_project="trading-bot-445817",
        registry_path="twirl",
    ),
    cloud_runtime=twirl.GcpCloudRuntime(
        project="trading-bot-445817",
        location="europe-west2",
        job_runner_account="twirl-runner@trading-bot-445817.iam.gserviceaccount.com",
        job_manager_account="twirl-job-manager@trading-bot-445817.iam.gserviceaccount.com",
        default_job_resource_config=twirl.CloudRunResourceConfig(
            memory="1Gi", cpu_count=1
        ),
    ),
)
