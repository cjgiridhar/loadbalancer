import os
from multiprocessing import Process

from flask import Flask, make_response, redirect

from balancer import STRATEGIES, LoadBalancer

app = Flask(__name__)
nodes = ['http://localhost:8000', 'http://localhost:8001']
lb = LoadBalancer(STRATEGIES.ROUND_ROBBIN)


@app.route('/')
def init():
    lb.startHealthCheck(nodes)
    # you could also do health check in the background
    # process = Process(
    #     target=lb.startHealthCheck,
    #     args=(nodes,),)
    # process.start()
    response = make_response("Load Balancer is Up!", 200)
    response.mimetype = "text/plain"
    return response


@app.route('/<string:var>')
def hello(var):
    node = lb.getNextNode()
    return redirect(node, code=302)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
