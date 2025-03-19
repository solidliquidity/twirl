#!/usr/bin/env bash

set -e
set -u
set -o pipefail

needed_services=("artifactregistry.googleapis.com" "bigquery.googleapis.com" "cloudapis.googleapis.com" "cloudbuild.googleapis.com" "iam.googleapis.com" "iamcredentials.googleapis.com" "run.googleapis.com" "secretmanager.googleapis.com" "sqladmin.googleapis.com" "storage.googleapis.com" "firestore.googleapis.com" "cloudfunctions.googleapis.com")

for service_api in ${needed_services[@]}; do
    gcloud --project ${TWIRL_GCP_PROJECT_ID} services enable $service_api
done
