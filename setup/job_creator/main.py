from __future__ import annotations

import os
from typing import TYPE_CHECKING

import functions_framework  # type: ignore[reportMissingImports]
from google.api_core.exceptions import GoogleAPICallError
from google.cloud import run_v2
from google.cloud.run_v2 import JobsClient
from google.cloud.run_v2.types import Job

if TYPE_CHECKING:
    import flask  # type: ignore[reportMissingModuleSource]


# Global scope for CF optimization: https://cloud.google.com/functions/docs/bestpractices/networking#accessing_google_apis
jobs_client = JobsClient()


@functions_framework.http
def run_job(request: flask.Request) -> flask.typing.ResponseReturnValue:  # type: ignore[name-defined]
    if request.method != "POST":
        return "", 405

    allowed_prefixes_str = os.environ.get("ALLOWED_IMAGE_PREFIXES")
    if not allowed_prefixes_str:
        raise LookupError("Required ENV variable 'ALLOWED_IMAGE_PREFIXES' not set")

    allowed_prefixes = allowed_prefixes_str.split()
    if len(allowed_prefixes) == 0:
        raise ValueError("'ALLOWED_IMAGE_PREFIXES' is empty, must allow at least one image prefix")
    for s in allowed_prefixes:
        if not s:
            raise ValueError("Empty string is not allowed as an allowed prefix (would allow all images)")
        if not s.endswith("/"):
            raise ValueError("Allowed prefix must end with a slash")

    job_request = None
    try:
        job_request = run_v2.CreateJobRequest.from_json(request.get_data(), ignore_unknown_fields=True)
        if not isinstance(job_request, run_v2.CreateJobRequest):
            raise TypeError(f"Expected CreateJobRequest, got {type(job_request)}")
    except Exception as e:
        print(f"Exception creating job request: {e}")
        return "Could not parse job request", 400

    containers = job_request.job.template.template.containers
    for container in containers:
        image = container.image
        allowed = any(image.startswith(p) for p in allowed_prefixes)
        if not allowed:
            return {"error": f"Image '{image}' not allowed"}, 403

    try:
        result = jobs_client.create_job(job_request).result()
        return Job.to_json(result)
    except GoogleAPICallError as e:
        return str(e), e.code if hasattr(e, "code") else 503
    except Exception as e:
        return f"unknown error: {e}", 500
