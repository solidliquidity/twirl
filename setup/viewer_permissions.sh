#!/usr/bin/env bash

set -e
set -u
set -o pipefail

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
        

: ${TWIRL_GCP_PROJECT_ID:="twirldata-prod"}
export TWIRL_GCP_PROJECT_ID

viewer_roles=("roles/run.viewer" "roles/logging.viewer" "roles/cloudbuild.builds.viewer")
for viewer_role in ${viewer_roles[@]}; do
    gcloud --project ${TWIRL_GCP_PROJECT_ID} projects add-iam-policy-binding ${TWIRL_GCP_PROJECT_ID} --member="group:twirl-developer-support@twirldata.com" --role="${viewer_role}" --condition=None
done
