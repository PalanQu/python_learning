import kubernetes.client as client
import kubernetes.config as config
import kubernetes.client.rest as rest
import kubernetes.stream.stream as stream
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger("kubernetes-api")

def list_pods():
    """
    list information of all pods
    :return:
    """
    corev1 = client.CoreV1Api()
    logger.info(corev1.list_pod_for_all_namespaces())

def list_deployment():
    """
    list information of all deployment
    :return:
    """
    appv1 = client.AppsV1Api()
    logger.info(appv1.list_deployment_for_all_namespaces())

def list_replicasets():
    """
    list all replica sets
    :return:
    """
    appv1 = client.AppsV1Api()
    logger.info(appv1.list_replica_set_for_all_namespaces())

def list_services():
    """
    list all services
    :return:
    """
    corev1 = client.CoreV1Api()
    logger.info(corev1.list_service_for_all_namespaces())


def create_deployment(name, *, containers, replicas, volumes, affinity={}, labels={}):
  '''
    Create a redis deployment.

    name: Name of the deployment.
    replicas: Number of replicas.
    containers: A list V1Pod or dictionaries with the same structure.
    volumes: A list of V1Pod or dictionaries with the same structure.
    affinity: Affinity spec dictionary.
    labels: A dictionary of key-value pairs.  Additional labels to attach to
        this deployment.  By default, the created deployment is labeled with
        `app=name`.  You may use this argument to override the existing label
        and/or add new labels.

    return: The deployment created.  None if the deployment cannot be created.
    '''
  api = client.AppsV1beta1Api()
  try:
    deployment = api.create_namespaced_deployment(
        namespace='default',
        body={
            'apiVersion': 'apps/v1beta1',
            'kind': 'Deployment',
            'metadata': {
                'name': name
            },
            'spec': {
                'replicas': replicas,
                'template': {
                    'metadata': {
                        'labels': labels
                    },
                    'spec': {
                        'affinity': affinity,
                        'containers': containers,
                        'volumes': volumes,
                    }
                }
            }
        }
    )
    return deployment
  except client.rest.ApiException as e:
    # XXX (zhongming): Prior to Kubernetes 1.7.8, the reason for trying to
    # create a deployment that already exists was 'AlreadyExists'.  Starting
    # with Kubernetes 1.7.8, the reason was changed to 'Conflict'.
    if e.reason == 'Conflict':
      logging.warning("Deployment '%s' already exists." % name)
    else:
      raise

def create_container_json(container_name, *, image, mount_path, mount_name, command, args, ports):
    """
    create a container json
    :param container_name:str the name of the container
    :param image:str: the image which the container use, ex:ubuntu:latest
    :param mounth_path:str: mount path
    :param mounth_name:str: mount name
    :param command:list[str]: command
    :param args:list[str]: the args of the command
    :param ports:dist: a dist format of port
    :return:
    """
    container = [
        {
            "name": container_name,
            "image": image,
            "volumnsMounts": [
                {
                    "name": mount_name,
                    "mountPath": mount_path
                }
            ],
            "command": command,
            "args": args,
            "ports": ports
        }
    ]
    return container

def create_volumns_json(volumns_name, *, configMap):
    """
    create volumns json
    :param volumns_name: volumn name
    :param configMap: a dist format of configmap
    :return:
    """
    volumns = [
        {
            "name": volumns_name,
            "configMap": configMap
        }
    ]
    return volumns

def create_configmap_json(configmap_name, *, key, path):
    """
    create configmap json
    :param configmap_name: configmap name
    :param key: configmap key
    :param path: configmap path
    :return:
    """
    configmap = {
        "name": configmap_name,
        "items": [
            {
                "key": key,
                "path": path
            }
        ]
    }
    return configmap

def create_configmap(name, *, config_content):
    """
    create config map
    :param name: configmap name
    :param config_content: config content
    :return:
    """
    api = client.CoreV1Api()
    body = {
        "data": {
            "redis-config": config_content
        },
        "metadata": {
            "name": name
        }
    }
    try:
        config_map = api.create_namespaced_config_map(namespace="default", body=body)
        return config_map
    except client.rest.ApiException as e:
        if e.reason == 'Conflict':
            logger.warning("configmap '%s' already exists." % name)
        else:
            raise

def create_service(service_name, *, service_type="NodePort", ports, label, selector):
    """
    create a service
    :param service_name: service name
    :param service_type: service type
    :param ports: a dict of port format
    :param label:
    :param selector:
    :return:
    """
    api = client.CoreV1Api()
    body = {
        "metadata": {
            "labels": {
                "app": label
            },
            "name": service_name
        },
        "spec": {
            "type": service_type,
            "selector": {
                "app": selector
            },
            "ports": ports
        }

    }
    try:
        service = api.create_namespaced_service(namespace="default", body=body)
        return service
    except client.rest.ApiException as e:
        if e.reason == 'Conflict':
            logger.warning("service '%s' already exists." % service_name)
        else:
            raise

def exec_command():
    name = "redis-test-deployment-57cf47df57-2g66g"
    namespace = "default"
    command = "ls"
    # command = client.V1ExecAction(["ls"])
    api = client.CoreV1Api()

    exec_command = [
        '/bin/sh',
        '-c',
        'echo This message goes to stderr >&2; echo This message goes to stdout']
    resp = stream(api.connect_get_namespaced_pod_exec, name, 'default',
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    print("Response: " + resp)

    # Calling exec interactively.
    exec_command = ['/bin/sh']
    resp = stream(api.connect_get_namespaced_pod_exec, name, 'default',
                  command=exec_command,
                  stderr=True, stdin=True,
                  stdout=True, tty=False,
                  _preload_content=False)
    print(resp)
    commands = [
        "echo test1",
        "echo \"This message goes to stderr\" >&2",
    ]

def test_create_configmap():
    """
    test to create a configmap
    :return:
    """
    content = "appendonly yes" + "\n" + \
              "dir /data" + "\n" + \
              "cluster-enabled yes" + "\n" + \
              "cluster-node-timeout 5000" + "\n" + \
              "bind 0.0.0.0"
    configmap_name = "redis-cluster-config"
    create_configmap(configmap_name, config_content=content)



def test_create_service():
    """
    test to create a service
    :return:
    """
    service_name = "test-service"
    label = "redis"
    selector = "redis"
    service_type = "NodePort"
    ports = [
        {
            "name": "client","port": 6379
        },
        {
            "name": "gossip","port": 16379
        }
    ]
    r = create_service(
        service_name=service_name,
        service_type=service_type,
        ports=ports,
        label=label,
        selector=selector)
    logger.info(r)

def test_create_deployment():
    """
    test to create a deployment
    :return:
    """
    deployment_name = "redis-test-deployment"
    volumn_name = "config"
    container_name = "redis"
    image = "redis:cluster"
    mount_path = "/etc/redis"
    mount_name = "config"
    command = ["redis-server"]
    args = ["/etc/redis/redis.conf"]
    labels = {
        "app": "redis"
    }
    ports = [
        {
            "name": "client",
            "containerPort": 6379
        },
        {
            "name": "gossip",
            "containerPort": 16379
        }
    ]
    configmap = create_configmap_json(
        configmap_name="redis-cluster-config",
        key="redis-config",
        path="redis.config")

    volumns = create_volumns_json(volumns_name=volumn_name, configMap=configmap)

    container = create_container_json(
        container_name=container_name,
        image=image,
        mount_path=mount_path,
        mount_name=mount_name,
        command=command,
        args=args,
        ports=ports)

    create_deployment(
        name=deployment_name,
        containers=container,
        replicas=6,
        volumes=volumns,
        labels=labels)

if __name__ == "__main__":
    config.load_kube_config()
    # test_apply_deployment()
    # test_apple_configmap()
    exec_command()
    # test_create_service()
