#!/usr/bin/env bash

set -e
set -u
set -o pipefail

# Check for gcloud command
if ! command -v gcloud &>/dev/null; then
    echo "gcloud command not found"
fi

if [ -z ${TWIRL_GCP_PROJECT_ID+x} ]; then
    echo "TWIRL_GCP_PROJECT_ID is not set"
    exit 1
fi

if [ -z ${TWIRL_GCP_LOCATION+x} ]; then
    echo "TWIRL_GCP_LOCATION is not set"
    exit 1
fi

if [ -z ${TWIRL_SERVICE_ACCOUNT+x} ]; then
    echo "TWIRL_SERVICE_ACCOUNT is not set"
    exit 1
fi