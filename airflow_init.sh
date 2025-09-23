#!/bin/bash

clear
printf "Hunter-Labs Airflow 3 AWS Kickstart\n"
printf "Python version: $(python --version)\n"
printf "Airflow version: $(airflow version)\n\n"

# Check for environment argument, you can change these to suit your local setup
if [[ $# -eq 0 ]] ; then
    echo 'ERROR - You must pass environment argument to initialise toolkit MUST be one of hunter-labs|your-local-env'
    exit 1
fi

printf "Setting PYTHONPATH\n\n"
export PYTHONPATH=$(pwd)/dags

printf "Setting local Airflow config\n\n"
export AIRFLOW_HOME=$(pwd)
export AIRFLOW__API__EXPOSE_CONFIG=True
export AIRFLOW__CORE__ALLOWED_DESERIALIZATION_CLASSES="airflow.* models.*"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__LOGGING__LOGGING_LEVEL="INFO"


printf "Setting up AWS config\n\n"
if [[ "$1" == "hunter-labs" ]]; then
    printf "Setting Hunter-Labs AWS_PROFILE\n\n"
    export AWS_PROFILE=default
fi
if [[ "$1" == "your-local-env" ]]; then
    printf "Setting Your-Local-Env AWS_PROFILE\n\n"
    export AWS_PROFILE=profile-goes-here
fi


# Config to reduce Airflow Caching AWS credentials and speed up failure feedback
export AWS_RETRY_MODE=standard
export AWS_MAX_ATTEMPTS=2
export NO_PROXY=localhost,127.0.0.1,::1
unset HTTP_PROXY
unset HTTPS_PROXY
printf "AWS Profile: ${AWS_PROFILE}\n\n"


printf "Starting Airflow 3 Standalone...\n\n"

sleep 3
airflow standalone
