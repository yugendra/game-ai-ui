import docker
from helper import get_port, get_ssh_port
import os

def create_env(user,projectname):
    vnc_port, info_channel = get_port()
    ssh_port = get_ssh_port()
    script_dir = os.path.dirname(os.path.realpath(__file__))

    if not vnc_port or not info_channel:
        return False
    if projectname == "R":
        return  run_r(user,projectname,vnc_port,ssh_port,script_dir,info_channel)
    if projectname == "pacman":
        return  run_pacman(user,projectname,vnc_port,ssh_port,script_dir,info_channel)
    if projectname == "antivirus":
        return  run_antivirus(user,projectname,vnc_port,ssh_port,script_dir,info_channel)
    if projectname == "speechrecognition":
        return  run_speechrecognition(user,projectname,vnc_port,ssh_port,script_dir,info_channel)
#################################### speechrecognition ##############################################
def run_speechrecognition(user,projectname,vnc_port,ssh_port,script_dir,info_channel):
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        env_image = 'speechrecognition:latest'
        language = "python3"
        volume1 = script_dir + '/user_agents/' + user + '/speech_recognition/'
        print(volume1)

        volumes= [ script_dir + '/user_agents/' + user + '/speech_recognition/' ]
        volume_bindings = {
                    script_dir + '/user_agents/' + user + '/speech_recognition/': {
                        'bind': '/home/ubuntu/speech_recognition',
                        'mode': 'rw',
                    },
        }

        host_config = client.create_host_config(
            binds=volume_bindings,
            port_bindings={

                22   : ssh_port,
                8888   : vnc_port,
            },
            privileged=True,
            ipc_mode='host',
            auto_remove=True

        )
        container_id = client.create_container(env_image, name=user, detach=True, ports=[22,8888], host_config=host_config,volumes=volumes,)
        print(container_id['Id'])
        client.start(container_id['Id'])
        print("cnt lanched")
        return vnc_port, info_channel, ssh_port, container_id['Id']
    except:
        return False, False, False, False


################################### PACMAN ##############################################
def run_pacman(user,projectname,vnc_port,ssh_port,script_dir,info_channel):
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        env_image = 'golucky5/pacman:latest'
        language = "python3"
        volume1 = script_dir + '/user_agents/' + user + '/pacman'
        #cmd = [ "/bin/sh", "-c","service ssh start && tail -F /root/projectdata/agent_log" ]
        host_config = client.create_host_config(
            port_bindings={
               
                22   : ssh_port,
                80   : vnc_port,
            },
            privileged=True,
            ipc_mode='host',
            auto_remove=True
        )
      
        container_id = client.create_container(env_image, name=user, detach=True, ports=[22,80], host_config=host_config)
        print(container_id['Id'])
        client.start(container_id['Id'])
        print("cnt lanched")
        return vnc_port, info_channel, ssh_port, container_id['Id']
    except:
        return False, False, False, False
#################################### Anti-virus ##############################################
def run_antivirus(user,projectname,vnc_port,ssh_port,script_dir,info_channel):
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        env_image = 'antivirus:latest'
        language = "python3"
        volume1 = script_dir + '/user_agents/' + user + '/antivirus/'
        print(volume1)

        volumes= [ script_dir + '/user_agents/' + user + '/antivirus/' ]
        volume_bindings = {
                    script_dir + '/user_agents/' + user + '/antivirus/': {
                        'bind': '/home/ubuntu/antivirus',
                        'mode': 'rw',
                    },
        } 

        host_config = client.create_host_config(
            binds=volume_bindings,
            port_bindings={

                22   : ssh_port,
                8888   : vnc_port,
            },
            privileged=True,
            ipc_mode='host',
            auto_remove=True

        )



        '''       
        #cmd = [ "/bin/sh", "-c","service ssh start && tail -F /root/projectdata/agent_log" ]
        host_config = client.create_host_config(
            port_bindings={

                22   : ssh_port,
                8888   : vnc_port,
            },
            privileged=True,
            ipc_mode='host',
            auto_remove=True
        )
        binds=[
                volume1  + ':/home/ubuntu/',
            ]
        '''

        container_id = client.create_container(env_image, name=user, detach=True, ports=[22,8888], host_config=host_config,volumes=volumes,)
        print(container_id['Id'])
        client.start(container_id['Id'])
        print("cnt lanched")
        return vnc_port, info_channel, ssh_port, container_id['Id']
    except:
        return False, False, False, False

################################# R programming #################################################
def run_r(user,projectname,vnc_port,ssh_port,script_dir,info_channel):
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        env_image = 'yugendra/ssh'
        language = "python3"
        cmd = [ "/bin/sh", "-c","service ssh start && tail -F /root/projectdata/agent_log" ]
        if projectname == "R":
            volume1 = script_dir + '/user_agents/' + user + '/rdata'
        if projectname == 'sentimentalnalysis':
            volume1 = script_dir + '/user_agents/' + user + '/moviereviewdata'
        if projectname == 'antivirus':
            volume1 = script_dir + '/user_agents/' + user + '/antivirusdata'
        volume2 = script_dir + '/DeepLearningMovies/' 
        host_config = client.create_host_config(
            port_bindings={
                6081 : vnc_port,
                22   : ssh_port
            },
            privileged=True,
            ipc_mode='host',
            auto_remove=True,
            binds=[
                volume1  + ':/root/projectdata',
                volume2  + ':/root/SentimentalAnalysis'
            ]
        )

        container_id = client.create_container(env_image, name=user, detach=True, ports=[6081,22,80], volumes=['/root/projectdata','/root/SentimentalAnalysis'], host_config=host_config, command=cmd)
        print(container_id['Id'])
        client.start(container_id['Id'])
        return vnc_port, info_channel, ssh_port, container_id['Id']
    except:
        return False, False, False, False

def execute_code( user, projectname):
     try:
       if projectname == "R":
           os.system('docker exec -ti '+user+' /bin/bash -c "Rscript /root/projectdata/script.R &> /root/projectdata/exec.log"')
     except:
        return False
          
def remove_env(user):
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        container_id  = client.stop(user)
        print("running container deleted ")
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

def get_host_ssh_port(user):
    try:
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        return client.inspect_container(user)['NetworkSettings']['Ports']['22/tcp'][0]['HostPort']
    except:
        return "0"
#create_env("user5","antivirus")
