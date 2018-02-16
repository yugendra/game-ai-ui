import docker
from helper import get_port


def create_env(user):
    vnc_port, info_channel = get_port()

    if not vnc_port or not info_channel:
        return False

    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        env_image = 'quay.io/openai/universe.flashgames:0.20.28'
        host_config = client.create_host_config(
            port_bindings={
                5900: vnc_port,
                15900: info_channel
            },
            privileged=True,
            ipc_mode='host',
            auto_remove=True
        )

        container_id = client.create_container(env_image, name=user, detach=True, host_config=host_config)

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

def is_env_running(user):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    try:
        container = client.containers.get(user)
        return True
    except:
        return False

