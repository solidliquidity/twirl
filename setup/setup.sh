#!/usr/bin/env bash

set -e
set -u
set -o pipefail
set -x

if [ "${BASH_VERSINFO:-0}" -lt 3 ]; then
    echo "bash version 3 or higher is required."
    exit 1
fi


export GITHUB_ORG="solidliquidity"
export GITHUB_REPO="twirl"
export TWIRL_GCP_LOCATION="europe-west2"
export TWIRL_GCP_PROJECT_ID="trading-bot-445817"
export DATASTORE_GCP_PROJECT_ID="trading-bot-445817"
export DATASTORE_GCP_LOCATION="europe-west2"
export TWIRL_SERVICE_ACCOUNT="porc-solid-liquidity@porc-prod.iam.gserviceaccount.com"
export WORKLOAD_IDENTITY_POOL_NAME="gh-twirl"
export WORKLOAD_IDENTITY_PROVIDER_NAME="gh-twirl-solidliquidity"
        


export build_account="twirl-builder"
export run_account="twirl-runner"
export manager_account="twirl-job-manager"
export job_creator_account="twirl-job-creator"

export builder_email="${build_account}@${TWIRL_GCP_PROJECT_ID}.iam.gserviceaccount.com"
export manager_email="${manager_account}@${TWIRL_GCP_PROJECT_ID}.iam.gserviceaccount.com"

bash check_local_env.sh
bash enable_apis.sh
bash account_setup.sh
bash container_registry_setup.sh
bash workload_identity_federation.sh
bash add_datastore_project_permissions.sh
bash add_job_creator.sh

echo "Setup complete!"
