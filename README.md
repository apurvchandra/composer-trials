While you cannot directly pass data to a DAG using gcloud commands, you can achieve similar functionality through the following approaches:

1. Triggering DAG with configuration:

You can trigger a DAG and pass data as runtime configuration using the --conf flag with the gcloud command. Here's an example:

gcloud beta composer environments run my-environment \
   --location=us-central1 \
   trigger_dag -- \
   -c '{"key1": "value1", "key2": "value2"}' my-dag
This command triggers the my-dag in the my-environment located in the us-central1 region. The -c flag with JSON data defines the configuration key-value pairs accessible within the DAG using {{ dag_run.conf['key'] }} syntax.

2. Cloud Storage and environment variables:

Store your data in a JSON file within Cloud Storage. During DAG execution, access the file using a task (e.g., GCPTransferOperator) and parse the data. Extract relevant values and set them as environment variables within the task using Python libraries like os. These environment variables can then be accessed by subsequent tasks within the DAG.


Python Code for POC

from airflow import DAG
from airflow.providers.google.cloud.operators.gke_start_pod import GKEStartPodOperator

with DAG(dag_id="my_dag", start_date=datetime(2024, 3, 3)) as dag:

    config_data = "{{ dag_run.conf }}"  # Access the configuration

    # Extract values from the configuration
    my_var1 = config_data.get("key1", "default_value1")
    my_var2 = config_data.get("key2", "default_value2")

    # Pass values to the operator
    task = GKEStartPodOperator(
        task_id="my_task",
        name="my_pod",
        namespace="default",
        image="ubuntu",
        env_vars={
            "MY_VAR1": my_var1,
            "MY_VAR2": my_var2,
        },
    )
