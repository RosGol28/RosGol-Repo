from kubernetes import client, config
from datetime import datetime, timedelta

def find_old_deployments(days=30):
    config.load_kube_config()

    apps_v1 = client.AppsV1Api()

    deployments = apps_v1.list_deployment_for_all_namespaces()

    now = datetime.now()

    old_deployments = []

    for deployment in deployments.items:
        creation_time = deployment.metadata.creation_timestamp

        if creation_time:
            creation_time_dt = creation_time.replace(tzinfo=None)

            if now - creation_time_dt > timedelta(days=days):
                old_deployments.append({
                    'name': deployment.metadata.name,
                    'namespace': deployment.metadata.namespace,
                    'creation_time': creation_time_dt.strftime('%Y-%m-%d %H:%M:%S')
                })

    return old_deployments

if __name__ == "__main__":
    old_deployments = find_old_deployments()

    if old_deployments:
        print("Old Deployments (older than 30 days):")
        for deployment in old_deployments:
            print(f"Deployment Name: {deployment['name']}, Namespace: {deployment['namespace']}, Created At: {deployment['creation_time']}")
    else:
        print("No deployments found that are older than 30 days.")
