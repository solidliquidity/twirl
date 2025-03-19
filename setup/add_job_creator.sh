#!/usr/bin/env bash

set -e
set -u
set -o pipefail

TWIRL_JOB_CREATOR_ID="twirl-job-creator"
manager_email="${manager_account}@${TWIRL_GCP_PROJECT_ID}.iam.gserviceaccount.com"
job_creator_email="${job_creator_account}@${TWIRL_GCP_PROJECT_ID}.iam.gserviceaccount.com"

gcloud --project ${TWIRL_GCP_PROJECT_ID} functions deploy ${TWIRL_JOB_CREATOR_ID} \
  --gen2 \
  --memory=256Mi \
  --cpu=0.083 \
  --no-allow-unauthenticated \
  --service-account=${job_creator_email} \
  --region=${TWIRL_GCP_LOCATION} \
  --runtime=python312 \
  --source=job_creator/ \
  --entry-point=run_job \
  --trigger-http \
  --timeout=30s \
  --set-env-vars ALLOWED_IMAGE_PREFIXES=${TWIRL_GCP_LOCATION}-docker.pkg.dev/${TWIRL_GCP_PROJECT_ID}/twirl/

gcloud --project ${TWIRL_GCP_PROJECT_ID} functions add-invoker-policy-binding ${TWIRL_JOB_CREATOR_ID} --region=${TWIRL_GCP_LOCATION} --member="serviceAccount:${manager_email}"
