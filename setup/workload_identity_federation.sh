#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

# Script to setup Workload Identity Federation for GitHub Actions
# Based on "official" notes from Google
#
# https://github.com/google-github-actions/auth?tab=readme-ov-file#workload-identity-federation-through-a-service-account

if [ -z ${TWIRL_GCP_PROJECT_ID+x} ]; then echo "TWIRL_GCP_PROJECT_ID is not set" && exit 1; fi
if [ -z ${TWIRL_GCP_LOCATION+x} ]; then echo "TWIRL_GCP_LOCATION is not set" && exit 1; fi
if [ -z ${GITHUB_ORG+x} ]; then echo "GITHUB_ORG is not set" && exit 1; fi
if [ -z ${GITHUB_REPO+x} ]; then echo "GITHUB_REPO is not set" && exit 1; fi
if [ -z ${WORKLOAD_IDENTITY_POOL_NAME+x} ]; then echo "WORKLOAD_IDENTITY_POOL_NAME is not set" && exit 1; fi
if [ -z ${WORKLOAD_IDENTITY_PROVIDER_NAME+x} ]; then echo "WORKLOAD_IDENTITY_PROVIDER_NAME is not set" && exit 1; fi

# Check if workload identity pool exists
if ! gcloud iam workload-identity-pools describe "${WORKLOAD_IDENTITY_POOL_NAME}" --project="${TWIRL_GCP_PROJECT_ID}" --verbosity critical --location="global"; then
  echo "Creating Workload Identity Pool: ${WORKLOAD_IDENTITY_POOL_NAME}"
  gcloud iam workload-identity-pools create "${WORKLOAD_IDENTITY_POOL_NAME}" \
  --project="${TWIRL_GCP_PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Twirl Release" \
  --quiet
else
    echo "Workload Identity Pool: ${WORKLOAD_IDENTITY_POOL_NAME} exists already!"
fi

WORKLOAD_IDENTITY_POOL_ID=$(gcloud iam workload-identity-pools describe "${WORKLOAD_IDENTITY_POOL_NAME}" --verbosity critical --project="${TWIRL_GCP_PROJECT_ID}" --location="global" --format="value(name)")

if ! gcloud iam workload-identity-pools providers describe "${WORKLOAD_IDENTITY_PROVIDER_NAME}" --location="global" --verbosity critical --project="${TWIRL_GCP_PROJECT_ID}" --workload-identity-pool="${WORKLOAD_IDENTITY_POOL_NAME}"; then
  echo "Creating OpenID Connect Workload Identity Provider: ${WORKLOAD_IDENTITY_PROVIDER_NAME}"
    # Create Identity Provider in pool
  gcloud iam workload-identity-pools providers create-oidc "${WORKLOAD_IDENTITY_PROVIDER_NAME}" \
  --project="${TWIRL_GCP_PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="${WORKLOAD_IDENTITY_POOL_NAME}" \
  --display-name="Twirl GitHub OIDC" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository_owner == '${GITHUB_ORG}'" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --quiet
else
  echo "Workload Identity Provider: ${WORKLOAD_IDENTITY_PROVIDER_NAME} exists already!"
fi

echo "Granting Workload Identity User Role to twirl-builder service account."
echo "This allows Github Actions (for ${GITHUB_ORG}/${GITHUB_REPO}) to impersonate it."

# Allow Service account impersonation
gcloud iam service-accounts add-iam-policy-binding "twirl-builder@${TWIRL_GCP_PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${TWIRL_GCP_PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_ORG}/${GITHUB_REPO}"
