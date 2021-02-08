# loadbalancer
Load Balancer in Python. 
Uses flask to demonstrate the workings of a load balancer.

# Load balancer strategies
- Round Robbin
- Least Connections
- Sticky Sessions

# Code

Code for Registering Nodes and setting Load Balancer Strategy

```python
nodes = ['http://localhost:8000', 'http://localhost:8001']
lb = LoadBalancer(STRATEGIES.ROUND_ROBBIN)
```

Redirects the request to next appropriate node based on strategy

```python
@app.route('/<string:var>')
def hello(var):
    node = lb.getNextNode()
    return redirect(node, code=302)
```    
