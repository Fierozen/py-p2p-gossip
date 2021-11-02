import os
import random

from gossip.server import GossipServer

PROJECT = "gossip"
SERVICE = "node"


def generate_hostname(project, service, index):
    return "{project}_{service}_{index}_1".format(
        project=project, service=service, index=index
    )


def get_left_peer(node_id, num_nodes):
    if node_id == 1:
        return num_nodes

    return node_id - 1


def get_right_peer(node_id, num_nodes):
    if node_id == num_nodes:
        return 1

    return node_id + 1


def get_initial_peers(node_id, port, num_nodes):

    peer_a = (
        generate_hostname(PROJECT, SERVICE, get_left_peer(node_id, num_nodes))
        + f":{port}"
    )
    peer_b = (
        generate_hostname(PROJECT, SERVICE, get_right_peer(node_id, num_nodes))
        + f":{port}"
    )

    return [peer_a, peer_b]


def get_random_peers(port, num_nodes):
    """Generate 3 random peers.

    On a small sample size this fails to allocate a client for 2 out of 16
    """
    peers = []
    for peer in range(3):
        random_peer = (
            generate_hostname(PROJECT, SERVICE, random.randint(1, num_nodes))
            + f":{port}"
        )
        peers.append(random_peer)
    return peers


port = int(os.environ["PORT"])
node_id = int(os.environ["NODE_ID"])
num_nodes = int(os.environ["NUM_NODES"])

peers = get_initial_peers(node_id, port, num_nodes)
# peers = get_random_peers(port, num_nodes)

server = GossipServer(node_id, port, peers)
server.start()
