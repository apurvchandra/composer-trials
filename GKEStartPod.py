from airflow import models
from airflow.providers.google.cloud.operators.kubernetes_engine import (
    GKEStartPodOperator,
)
from airflow.utils.dates import days_ago


with models.DAG(
    "autopilot",
    schedule_interval=None,  # Override to match your needs
    start_date=days_ago(1),
    tags=["example"],
) as dag:
    # TODO(developer): update with your values
    PROJECT_ID = ""
    # It is recommended to use regional clusters for increased reliability
    # though passing a zone in the location parameter is also valid
    CLUSTER_REGION = "europe-west2"
    CLUSTER_NAME = "autopilot-cluster-1"
    #config_data = "{{ dag_run.conf }}"  # Access the configuration

    # Extract values from the configuration
    autopilot = "{{dag_run.conf['pilotmode']}}" 

    kubernetes_min_pod = GKEStartPodOperator(
        # The ID specified for the task.
        task_id="pod-autopilot",
        # Name of task you want to run, used to generate Pod ID.
        name="pod-ex-minimum",
        project_id=PROJECT_ID,
        location=CLUSTER_REGION,
        cluster_name=CLUSTER_NAME,
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=["echo"], 
        # The namespace to run within Kubernetes, default namespace is        
        namespace="default",
        # Execute Dag using // gcloud composer environments run my-cmp --location europe-west2 dags trigger -- -c '{"pilotmode":"deletepod"}'  autopilot
        env_vars={
            "pilotmode": autopilot,
        },
        get_logs=True,
        image="gcr.io/gcp-runtimes/ubuntu_18_0_4",
        on_finish_action="delete_pod",
    )

    kubernetes_min_pod
