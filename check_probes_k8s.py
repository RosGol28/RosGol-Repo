from kubernetes import client, config

def find_pods_without_probes():
    config.load_kube_config()

    v1 = client.CoreV1Api()

    pods = v1.list_pod_for_all_namespaces()

    pods_without_probes = []

    for pod in pods.items:
        for container in pod.spec.containers:
            if not container.liveness_probe and not container.readiness_probe:
                pod_info = {
                    'pod_name': pod.metadata.name,
                    'namespace': pod.metadata.namespace,
                    'container_name': container.name,
                    'image': container.image
                }
                pods_without_probes.append(pod_info)

    return pods_without_probes

if __name__ == "__main__":
    pods_without_probes = find_pods_without_probes()

    if pods_without_probes:
        print("Pods without readiness/liveness probes:")
        for pod in pods_without_probes:
            print(f" Namespace: {pod['namespace']}  Pod: {pod['pod_name']}  Container: {pod['container_name']} ")
    else:
        print("No pods found without readiness/liveness probes.")


