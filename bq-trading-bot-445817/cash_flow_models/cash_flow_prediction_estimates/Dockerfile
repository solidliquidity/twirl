ARG TWIRL_VERSION
FROM europe-docker.pkg.dev/twirldata/twirl/twirl-base:${TWIRL_VERSION}

ARG USER_ID=1011
ARG GROUP_ID=1011

RUN getent group ${GROUP_ID} || groupadd -g ${GROUP_ID} app && \
useradd -m -l -u ${USER_ID} -g ${GROUP_ID} app

ARG REQUIREMENTS_PATH=UNDEFINED
COPY --chmod=555  *${REQUIREMENTS_PATH} requirements.txt
RUN --mount=type=cache,target=/home/app/.cache \
    if [ "$REQUIREMENTS_PATH" = "UNDEFINED" ] ; then echo no requirements.txt provided ; else pip install --compile -r requirements.txt; fi

# Make sure to exclude file that should not be in the image through the .dockerignore file
COPY --chmod=755 . .

ARG DBT_PATH="UNDEFINED"

RUN if [ "$DBT_PATH" = "UNDEFINED" ] ; then echo skipping dbt setup ; else sh -c 'cd $DBT_PATH && dbt deps --log-level-file=none' ; fi

USER app
ARG GIT_COMMIT_HASH="unknown"
ENV GIT_COMMIT_HASH=${GIT_COMMIT_HASH}

# set ENV as late as possible, to avoid invalidating Docker cache layers above
ARG ENV
ENV ENV=${ENV}
