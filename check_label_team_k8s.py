from kubernetes import client, config

def get_namespaces():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    namespaces = v1.list_namespace().items
    return namespaces

def check_team_labels(namespaces):
    missing_labels = []
    for ns in namespaces:
        labels = ns.metadata.labels or {}
        if 'team' not in labels:
            missing_labels.append(ns.metadata.name)
    return missing_labels

if __name__ == "__main__":
    namespaces = get_namespaces()
    missing_team_labels = check_team_labels(namespaces)

    if missing_team_labels:
        print("Namespaces без label 'team':")
        for ns in missing_team_labels:
            print(f" - {ns}")
    else:
        print("Все namespaces имеют label 'team'")
