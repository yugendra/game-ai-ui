import docker
from helper import get_port
import os

def create_env(user, language="python3"):
    vnc_port, info_channel = get_port()
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if not vnc_port or not info_channel:
        return False

    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        env_image = 'yugendra/gym'
        cmd = [ "/bin/sh", "-c", language + " /root/gym_examples/agent.py > /root/gym_examples/agent_log 2>&1" ]
        volume = script_dir + '/user_agents/' + user
        host_config = client.create_host_config(
            port_bindings={
                6081 : vnc_port
            },
            privileged=True,
            ipc_mode='host',
            auto_remove=True,
            binds=[
                volume  + ':/root/gym_examples'
            ]
        )

        container_id = client.create_container(env_image, name=user, detach=True, ports=[6081], volumes=['/root/gym_examples'], host_config=host_config, command=cmd)

        client.start(container_id['Id'])
        return vnc_port, info_channel
    except:
        return False, False


def remove_env(user):
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        container_id  = client.stop(user)
        return True
    except:
        return False

def remove_env_in_bulk(users):
    try:
        for user in users:
            remove_env(user)
        return True
    except:
        return False

def is_env_running(user):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    try:
        container = client.containers.get(user)
        return True
    except:
        return False

def get_env_list():
    container_names = []
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    containers = client.containers.list()
    for c in containers:
        container_names.append(c.name)
    return container_names

def get_vnc_port(user):
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        return client.inspect_container(user)['NetworkSettings']['Ports']['6081/tcp'][0]['HostPort']
    except:
        return "0"

