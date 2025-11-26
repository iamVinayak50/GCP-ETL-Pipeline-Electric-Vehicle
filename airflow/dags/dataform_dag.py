from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataform import (
    DataformCreateCompilationResultOperator,
    DataformCreateWorkflowInvocationOperator,
)
from airflow.providers.google.cloud.sensors.dataform import DataformWorkflowInvocationStateSensor

PROJECT_ID = "boxwood-axon-470816-b1"
REGION = "us-central1"
REPO_ID = "dataform-demo1"
WORKSPACE_ID = "dev-vinayak"

with DAG(
    dag_id="trigger_dataform_workflow",
    schedule_interval=None,  # manual trigger
    start_date=days_ago(1),
    catchup=False,
    tags=["dataform"],
) as dag:

    # 1️⃣ Create Compilation Result
    create_compilation = DataformCreateCompilationResultOperator(
        task_id="create_compilation",
        project_id=PROJECT_ID,
        region=REGION,
        repository_id=REPO_ID,
        compilation_result={
            "workspace": f"projects/{PROJECT_ID}/locations/{REGION}/repositories/{REPO_ID}/workspaces/{WORKSPACE_ID}"
        },
    )

    # 2️⃣ Trigger Workflow Invocation
    trigger_workflow = DataformCreateWorkflowInvocationOperator(
        task_id="trigger_workflow",
        project_id=PROJECT_ID,
        region=REGION,
        repository_id=REPO_ID,
        workflow_invocation={
            "compilation_result": "{{ task_instance.xcom_pull('create_compilation')['name'] }}"
        },
    )


    create_compilation >> trigger_workflow 
