from kubernetes import client, config

def find_pods_without_requests_limits():
    config.load_kube_config()
    
    v1 = client.CoreV1Api()
    
    pods = v1.list_pod_for_all_namespaces(watch=False)

    pods_without_requests_limits = []

    for pod in pods.items:
        for container in pod.spec.containers:
            if (not container.resources.requests) and (not container.resources.limits):
                pods_without_requests_limits.append({
                    'namespace': pod.metadata.namespace,
                    'name': pod.metadata.name,
                    'container_name': container.name
                })

    return pods_without_requests_limits

if __name__ == "__main__":
    pods_without_requests_limits = find_pods_without_requests_limits()
    
    if not pods_without_requests_limits:
        print("All pods have req&lim")
    else:
        print("Pods without req&lim:")
        for pod in pods_without_requests_limits:
            print(f"Namespace: {pod['namespace']}  Pod: {pod['name']} Container: {pod['container_name']} ")
