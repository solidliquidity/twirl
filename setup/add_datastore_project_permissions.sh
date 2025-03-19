#!/usr/bin/env bash

set -e
set -u
set -o pipefail

TWIRL_RUNNER_EMAIL=twirl-runner@${TWIRL_GCP_PROJECT_ID}.iam.gserviceaccount.com
ROLE_TO_ADD=roles/bigquery.dataViewer

if [[ "$DATASTORE_GCP_PROJECT_ID" != "$TWIRL_GCP_PROJECT_ID" ]]; then
  gcloud --project ${DATASTORE_GCP_PROJECT_ID} projects add-iam-policy-binding ${DATASTORE_GCP_PROJECT_ID} \
    --member="serviceAccount:${TWIRL_RUNNER_EMAIL}" \
    --role="${ROLE_TO_ADD}"
fi
