# Load Balancer Stuff
import time
from enum import Enum

import requests

from pymemcache.client import base

client = base.Client(('0.0.0.0', 11211))
client.set('num_requests', 0)

# Declare Load Balancer Strategies


class STRATEGIES(Enum):
    ROUND_ROBBIN = 0,
    LEAST_CONNECTIONS = 1,
    STICKY_SESSIONS = 2

# Execute a Strategy


class Strategy:
    def __init__(self, strategy, requests, nodes):
        self.requests = requests
        self.nodes = nodes
        self.strategy = strategy

    def execute(self):
        if self.strategy == STRATEGIES.ROUND_ROBBIN:
            if not self.requests:
                return 0
            index = self.requests % len(self.nodes)
            return index

# Represents a Node that serves requests


class Node:
    def __init__(self, url, isAlive):
        self.isAlive = isAlive
        self.url = url

    def checkAlive(self):
        return self.isAlive

    def setAlive(self, status):
        self.isAlive = status

    def getURL(self):
        return self.url

    def __repr__(self):
        return self.getURL()

# Represents a Target Group that constitues Nodes


class TargetGroup:
    def __init__(self):
        self.targetGroup = []
        self.currentIndex = 0

    def registerNode(self, node):
        print("Registering Node", node)
        if node.checkAlive():
            self.targetGroup.append(node)

    def getNodes(self):
        return self.targetGroup

    def checkNodes(self, nodes):
        for x in nodes:
            n = Node(url=x, isAlive=True)
            self.registerNode(n)

        for n in self.targetGroup:
            print("Health check", n)
            r = requests.get(n.url)
            if r.status_code == 200:
                n.setAlive(True)


# Represents the Load Balancer
class LoadBalancer:

    def __init__(self, strategy):
        self.strategy = strategy
        self.tg = TargetGroup()

    def setStrategy(self, strategy):
        self.strategy = strategy

    def getStrategy(self):
        return self.strategy

    def startHealthCheck(self, nodes):
        print('Starting healthcheck', nodes)
        self.tg.checkNodes(nodes)

    def getNextNode(self):
        nodes = self.tg.getNodes()
        strategy = self.getStrategy()
        index = Strategy(
            strategy, int(
                client.get('num_requests')), nodes).execute()
        client.incr('num_requests', 1)
        return nodes[index]
