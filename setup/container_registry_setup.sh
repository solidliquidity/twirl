#!/usr/bin/env bash

set -e
set -u
set -o pipefail

if ! gcloud --project ${TWIRL_GCP_PROJECT_ID} --verbosity critical artifacts repositories describe twirl --location=${TWIRL_GCP_LOCATION}; then
    gcloud --project=${TWIRL_GCP_PROJECT_ID} artifacts repositories create twirl --repository-format=docker --location=${TWIRL_GCP_LOCATION}  --mode=standard-repository --repository-format=docker --description="Container repo for twirl project."
  else
    echo "Repository 'twirl' already exists, will not create it"
fi
