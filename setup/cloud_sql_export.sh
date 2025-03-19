#!/usr/bin/env bash

set -e
set -u
set -o pipefail

if [ "${BASH_VERSINFO:-0}" -lt 5 ]; then
    echo "bash version 3 or higher is required."
    exit 1
fi

if [ -z ${GS_BUCKET+x} ]; then
    echo "GS_BUCKET is not set"
    exit 1
fi

if [ -z ${TWIRL_GCP_PROJECT_ID+x} ]; then
    echo "TWIRL_GCP_PROJECT_ID is not set"
    exit 1
fi

if [ -z ${TWIRL_GCP_LOCATION+x} ]; then
    echo "TWIRL_GCP_LOCATION is not set"
    exit 1
fi

if [ -z ${CLOUD_SQL_INSTANCE+x} ]; then
    echo "CLOUD_SQL_INSTANCE is not set"
    exit 1
fi

export run_account="twirl-runner"
run_email="${run_account}@${TWIRL_GCP_PROJECT_ID}.iam.gserviceaccount.com"

if ! gcloud --project ${TWIRL_GCP_PROJECT_ID} storage buckets describe gs://${GS_BUCKET}; then
    gcloud --project ${TWIRL_GCP_PROJECT_ID} storage buckets create gs://${GS_BUCKET} --location=${TWIRL_GCP_LOCATION} --public-access-prevention --uniform-bucket-level-access
fi

gcloud --project ${TWIRL_GCP_PROJECT_ID} storage buckets add-iam-policy-binding gs://${GS_BUCKET} --member=serviceAccount:${run_email} --role=roles/storage.objectAdmin

echo "Please manually add the follow permissions:"
echo "Give the role Cloud SQL Admin (roles/cloudsql.admin) to ${run_email} for ${CLOUD_SQL_INSTANCE} in project ${TWIRL_GCP_PROJECT_ID}"
echo "Give the role Storage Admin (roles/storage.admin) to the Service Account used in ${CLOUD_SQL_INSTANCE} for the GCS bucket ${GS_BUCKET} in project ${TWIRL_GCP_PROJECT_ID}"
