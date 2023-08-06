MLFLOW_SERVICE = "MlflowService"
MLFLOW_API_GET_RUN = "GetRun"
MLFLOW_API_LIST_ARTIFACTS = "ListArtifacts"

DATABRICKS_MLFLOW_ARTIFACTS_SERVICE = "DatabricksMlflowArtifactsService"
DATABRICKS_MLFLOW_API_GET_CREDENTIALS_FOR_WRITE = "GetCredentialsForWrite"
DATABRICKS_MLFLOW_API_GET_CREDENTIALS_FOR_READ = "GetCredentialsForRead"

_SERVICE_AND_API_TO_INFO = {
    MLFLOW_SERVICE: {
        MLFLOW_SERVICE: {
            MLFLOW_API_GET_RUN: ('/api/2.0/mlflow/runs/get', 'GET'),
            MLFLOW_API_LIST_ARTIFACTS: ('/api/2.0/mlflow/artifacts/list', 'GET'),
        },
        DATABRICKS_MLFLOW_ARTIFACTS_SERVICE: {
            DATABRICKS_MLFLOW_API_GET_CREDENTIALS_FOR_WRITE: ('/api/2.0/mlflow/artifacts/credentials-for-write', 'GET'),
            DATABRICKS_MLFLOW_API_GET_CREDENTIALS_FOR_READ: ('/api/2.0/mlflow/artifacts/credentials-for-read', 'GET'),
        }
    }
}


def get_service_api_info(service, api):
    return _SERVICE_AND_API_TO_INFO[service][api]

