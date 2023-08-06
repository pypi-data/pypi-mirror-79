from agent.commands.docker_commands import docker_compose_up, docker_compose_pull
from agent.config.properties import ROOT_DIR
from agent.constants import DOCKER_COMPOSE_FILE


def setup_rabbitmq():
    docker_compose_path = f"{ROOT_DIR}/{DOCKER_COMPOSE_FILE}"
    docker_compose_pull(path=docker_compose_path)
    docker_compose_up(path=docker_compose_path)
