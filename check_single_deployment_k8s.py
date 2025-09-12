from kubernetes import client, config

def find_single_instance_pods():
    config.load_kube_config()

    v1 = client.CoreV1Api()

    pods = v1.list_pod_for_all_namespaces()

    single_instance_pods = {}

    for pod in pods.items:
        namespace = pod.metadata.namespace
        pod_name = pod.metadata.name
        
        if namespace not in single_instance_pods:
            single_instance_pods[namespace] = {}
        
        if pod_name not in single_instance_pods[namespace]:
            single_instance_pods[namespace][pod_name] = 0
        
        single_instance_pods[namespace][pod_name] += 1

    result = []
    for namespace, pods in single_instance_pods.items():
        for pod_name, count in pods.items():
            if count == 1:
                result.append({
                    'pod_name': pod_name,
                    'namespace': namespace
                })

    return result

if __name__ == "__main__":
    single_instance_pods = find_single_instance_pods()

    if single_instance_pods:
        print("Pods deployed in a single instance:")
        for pod in single_instance_pods:
            print(f"Pod Name: {pod['pod_name']}, Namespace: {pod['namespace']}")
    else:
        print("No pods found that are deployed in a single instance.")
