# Airflow AWS Kickstart
A sample Airflow 3 DAG and initialization scripts to kickstart your Airflow + AWS data engineering journey and to hopefully help you get avoid common pitfalls.

Code can be adapted for your own use cases.

## Prerequisites
- [uv package manager](https://docs.astral.sh/uv/) must be installed
### Setup Virtual Environment
Run the following commands to create and activate a virtual environment using `uv`:
```bash
uv sync
source ./.venv/bin/activate
```

## Starting Airflow 3
To start Airflow, use the `airflow_init.sh` script and provide your local environment as an argument, eg `hunter-labs` as illustrated below.  You can modify the script for your local env.
```bash
./airflow_init.sh hunter-labs
```

The `airflow_init.sh` script will start the Web UI.  If this is the first time running Airflow in your environment several config files will be generated. 

### Logging into the Airflow 3 Web UI
 Once Airflow is running, you can access the web UI at: http://localhost:8080.  This will take you to a login screen.

You can find the local admin password in the `simple_auth_manager_passwords.json.generated` file, which Airflow just generated.  Which is gitignored 

### Running the AWS Kickstart DAG
To successfully run the AWS Kickstart DAG the AWS Profile you supplied in the `airflow_init.sh` script must have permissions to List All S3 Buckets.

1. Click the Dags icon on the left hand side
2. Select the `aws_kickstart` DAG, and select `Trigger` in the top right hand corner.  The DAG Parameters popup will launch.  
3. You can toggle the List All Buckets button, if you set it to False you must supply the name of the bucket you want to list in the S3 Bucket Name fields instead.  Click `Trigger` to start the DAG run.
4. When running click on the logs icon to the see the output of the DAG run

### Airflow Config
Config for Airflow is located in `airflow.cfg`  Config can be overridden using environment variables as demonstrated in the `airflow_init.sh` script.

### Useful Airflow CLI Commands
```bash
## Reset the Airflow DB
airflow db reset --yes
```

### AWS SSO Session Reset 
Run the following to reset your local AWS session if Airflow is hanging.  Not required if you are using IAM Roles or a local IAM User Service Accounts
```bash
rm -rf ~/.aws/sso/cache/*
rm -rf ~/.aws/cli/cache/*
aws sso logout
aws sso login --sso-session your session
```
