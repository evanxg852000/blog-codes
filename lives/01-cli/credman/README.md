steps 
python3 -m venv venv

pip install --editable .

pip install pytest

```python
def strong(fn):
    def wrapper(x):
        return f'<strong>{fn(x)}</strong>'
    return wrapper

def emphasis(fn):
    def wrapper(x):
        return f'<em>{fn(x)}</em>'
    return wrapper


@strong
@emphasis
def greet(msg):
    return msg

print(greet('hello'))

#take arbitrary ags
def proxy(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) 
    return wrapper
```



```python
routes = {}

def route(path):
    #global routes
    def decorator(fn):
        routes[path] = fn
    return decorator

@route('home/')
def home(*args, **kwargs):
    print('handling home/')
    print(args, kwargs)

@route('about/')
def about(*args, **kwargs):
    print('handling about/')  
    print(args, kwargs)

print(routes['home/'](23, 4, ev=3))

```



## Unit test

```python 

def add(a, b):
    return a + b

class CircularBufferTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(5,4), 9)


if __name__ == '__main__':
    unittest.main()

```
