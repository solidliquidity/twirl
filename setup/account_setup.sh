#!/usr/bin/env bash

set -e
set -u
set -o pipefail

if ! gcloud --project ${TWIRL_GCP_PROJECT_ID} --verbosity critical iam service-accounts describe ${builder_email}; then
    builder_email=$(gcloud --project ${TWIRL_GCP_PROJECT_ID} --format='value(email)' iam service-accounts create ${build_account} --description "Used to build and publish new Twirl project containers" --display-name "Twirl Builder")
  else
    echo "twirl-builder IAM service account already exists, will not create it"
fi

builder_roles=("roles/cloudbuild.builds.builder" "roles/logging.logWriter" "roles/artifactregistry.writer")
for builder_role in ${builder_roles[@]}; do
    gcloud --project ${TWIRL_GCP_PROJECT_ID} projects add-iam-policy-binding ${TWIRL_GCP_PROJECT_ID} --member="serviceAccount:${builder_email}" --role="${builder_role}" --condition=None
done

run_email="${run_account}@${TWIRL_GCP_PROJECT_ID}.iam.gserviceaccount.com"
if ! gcloud --project ${TWIRL_GCP_PROJECT_ID} iam service-accounts describe ${run_email}; then
    run_email=$(gcloud --project ${TWIRL_GCP_PROJECT_ID} --format='value(email)' iam service-accounts create ${run_account} --description "Used by Twirl process your data" --display-name "Twirl Runner")
fi

run_roles=("roles/bigquery.dataEditor" "roles/logging.logWriter" "roles/bigquery.jobUser" "roles/bigquery.readSessionUser")
for run_role in ${run_roles[@]}; do
    gcloud --project ${TWIRL_GCP_PROJECT_ID} projects add-iam-policy-binding ${TWIRL_GCP_PROJECT_ID} --member="serviceAccount:${run_email}" --role="${run_role}" --condition=None
done


if ! gcloud --project ${TWIRL_GCP_PROJECT_ID} --verbosity critical iam service-accounts describe ${manager_email}; then
    manager_email=$(gcloud --project ${TWIRL_GCP_PROJECT_ID} --format='value(email)' iam service-accounts create ${manager_account} --description "Used to Manage Twirl Jobs" --display-name "Twirl Job Manager")
  else
    echo "twirl-job-manager IAM service account already exists, will not create it"
fi

manager_role="TwirlManager"
if ! gcloud --project ${TWIRL_GCP_PROJECT_ID} --verbosity critical iam roles describe ${manager_role}; then
    gcloud --project ${TWIRL_GCP_PROJECT_ID} iam roles create ${manager_role} --project ${TWIRL_GCP_PROJECT_ID} --title "Twirl Manager" --description "Twirl Manager" --stage "GA" --permissions "run.jobs.get,run.jobs.list,run.jobs.delete,run.executions.delete,run.operations.delete,run.operations.get,run.jobs.run,run.jobs.runWithOverrides,run.services.delete,run.routes.invoke,run.executions.get"
  else
    echo "twirl-manager IAM service account already exists, will not create it"
fi

manager_roles=("projects/${TWIRL_GCP_PROJECT_ID}/roles/${manager_role}" "roles/logging.viewer")
for manager_role in ${manager_roles[@]}; do
    gcloud --project ${TWIRL_GCP_PROJECT_ID} projects add-iam-policy-binding ${TWIRL_GCP_PROJECT_ID} --member="serviceAccount:${manager_email}" --role="${manager_role}" --condition=None
done

job_creator_role="TwirlJobCreator"
if ! gcloud --project ${TWIRL_GCP_PROJECT_ID} --verbosity critical iam roles describe ${job_creator_role}; then
    gcloud --project ${TWIRL_GCP_PROJECT_ID} iam roles create ${job_creator_role} --project ${TWIRL_GCP_PROJECT_ID} --title "Twirl Job Creator" --description "Twirl Job Creator" --stage "GA" --permissions "run.jobs.create,run.jobs.update,run.services.create,run.operations.get,run.jobs.get"
    echo "twirl-job-creator IAM role doesn't exist, will create it"
else
    gcloud --project ${TWIRL_GCP_PROJECT_ID} iam roles update ${job_creator_role} --project ${TWIRL_GCP_PROJECT_ID} --title "Twirl Job Creator" --description "Twirl Job Creator" --stage "GA" --permissions "run.jobs.create,run.jobs.update,run.services.create,run.operations.get,run.jobs.get"
    echo "twirl-job-creator IAM role already exists, will update it"
fi


job_creator_email="${job_creator_account}@${TWIRL_GCP_PROJECT_ID}.iam.gserviceaccount.com"
if ! gcloud --project ${TWIRL_GCP_PROJECT_ID} --verbosity critical iam service-accounts describe ${job_creator_email}; then
    job_creator_email=$(gcloud --project ${TWIRL_GCP_PROJECT_ID} --format='value(email)' iam service-accounts create ${job_creator_account} --description "Used to Create Twirl Jobs" --display-name "Twirl Job Creator")
  else
    echo "twirl-job-creator IAM service account already exists, will not create it"
fi

job_creator_roles=("projects/${TWIRL_GCP_PROJECT_ID}/roles/${job_creator_role}")
for job_creator_role in ${job_creator_roles[@]}; do
    gcloud --project ${TWIRL_GCP_PROJECT_ID} projects add-iam-policy-binding ${TWIRL_GCP_PROJECT_ID} --member="serviceAccount:${job_creator_email}" --role="${job_creator_role}" --condition=None
done

gcloud --project ${TWIRL_GCP_PROJECT_ID} iam service-accounts add-iam-policy-binding ${manager_email} --member="serviceAccount:${TWIRL_SERVICE_ACCOUNT}" --role="roles/iam.serviceAccountTokenCreator"  --condition=None

gcloud --project ${TWIRL_GCP_PROJECT_ID} iam service-accounts add-iam-policy-binding ${run_email} --member="serviceAccount:${job_creator_email}" --role="roles/iam.serviceAccountUser" --condition=None
