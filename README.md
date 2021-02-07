# loadbalancer
Load Balancer in Python. 
Uses flask to demonstrate the workings of load balancer.

# Load balancer strategies
- Round Robbin
- Least Connections
- Sticky Sessions

# Code

Registering Nodes to Loadbalancer 
Setting Load Balancer Strategy

```python
nodes = ['http://localhost:8000', 'http://localhost:8001']
lb = LoadBalancer(STRATEGIES.ROUND_ROBBIN)
```

Redirects the request to next chosen node

```python
@app.route('/<string:var>')
def hello(var):
    node = lb.getNextNode()
    return redirect(node, code=302)
```    
