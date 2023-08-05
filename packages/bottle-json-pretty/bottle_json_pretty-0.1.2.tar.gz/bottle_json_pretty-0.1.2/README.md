# bottle-json-pretty #
A plugin for the [Bottle Web Framework](https://bottlepy.org) that returns pretty formatted JSON.
The plugin extends the default JSON formatter's behavior by adding the `indent` keyword argument to each call.
This is supported by at least the standard library [`json`][1], [`ujson`][2], and [`simplejson`][3] ([1][4], [2][5], [3][6]).

Indent level and formatting during production can be controlled via the initializer.

[1]: https://github.com/bottlepy/bottle/blob/533c2cd76039b4e22a5c36c0e97df82b37c63670/bottle.py#L84
[2]: https://github.com/bottlepy/bottle/blob/533c2cd76039b4e22a5c36c0e97df82b37c63670/bottle.py#L82
[3]: https://github.com/bottlepy/bottle/blob/8f9e66d4ab05ebd81a8ac50d9e265ef2e7d5066f/bottle.py#L109
[4]: https://docs.python.org/3/library/json.html#json.dumps
[5]: https://pypi.org/project/ujson/#indent
[6]: https://simplejson.readthedocs.io/en/latest/#simplejson.dumps

```python
from bottle import Bottle
from bottle_json_pretty import JSONPrettyPlugin

app = Bottle(autojson=False)
app.install(JSONPrettyPlugin(indent=2, pretty_production=True))

@app.get('/')
def bottle_test():
    return {
        'status': 'ok',
        'code': 200,
        'messages': [],
        'result': {
            'test': {
                'working': True
            }
        }
    }

app.run()
```