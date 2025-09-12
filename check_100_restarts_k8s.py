from kubernetes import client, config

def find_pods_with_restarts(threshold=100, namespace=None):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()

    v1 = client.CoreV1Api()

    if namespace:
        pods = v1.list_namespaced_pod(namespace)
    else:
        pods = v1.list_pod_for_all_namespaces()

    result = []
    for pod in pods.items:
        restart_count = sum([cs.restart_count for cs in pod.status.container_statuses or []])
        if restart_count > threshold:
            result.append({
                "namespace": pod.metadata.namespace,
                "name": pod.metadata.name,
                "restarts": restart_count
            })

    return result


if __name__ == "__main__":
    pods = find_pods_with_restarts(threshold=100)
    if not pods:
        print("All good, we haven't pods with 100 restarts yohou")
    else:
        print("Pods with more than 100 restarts:")
        for p in pods:
            print(f"Namespace: {p['namespace']} |  Pod: {p['name']} - restarts: {p['restarts']}")
