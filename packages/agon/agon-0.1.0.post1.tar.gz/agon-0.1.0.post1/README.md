# Agon

Agon is a thin wrapper around [jmespath](https://pypi.org/project/jmespath/) which let you to compose projections in a more natural manner.

It's usage is quite simple

```python
from agon import Agon

assert Agon("foo | bar") == Agon("foo") | Agon("bar") == Agon("foo") | "bar"
assert {"foo": {"bar": "baz"}} | Agon("foo | bar") == "baz"
assert {"foo": {"bar": "baz"}} | Agon("foo") | Agon("bar") == "baz"
assert {"foo": {"bar": "baz"}} | (Agon("foo") | "bar") == "baz"
```
