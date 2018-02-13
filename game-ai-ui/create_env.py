import docker
from helper import get_port


def create_env():
    client = docker.APIClient(base_url='unix://var/run/docker.sock')

    vnc_port, info_channel = get_port()

    if not vnc_port or not info_channel:
        return False

    try:
        env_image = 'quay.io/openai/universe.flashgames:0.20.28'
        host_config = client.create_host_config(
            port_bindings={
                5900: vnc_port,
                15900: info_channel
            },
            privileged=True,
            ipc_mode='host'
        )

        container_id = client.create_container(env_image, detach=True, host_config=host_config)

        client.start(container_id['Id'])
        return container_id['Id']
    except:
        return False


print create_env()
