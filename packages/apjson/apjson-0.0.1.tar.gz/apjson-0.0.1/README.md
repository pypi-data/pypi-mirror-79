# apjson

`apjson` is an asynchonus prettifier for json-like objects and a simple implementation of the `json` module and decorators.

## Example
```python
from apjson import prettify, to_bytesio, jbytesio, jpretty
import asyncio


@jbytesio(sort_keys=True, check_circular=True)
def sync_json():

    return '{"in": "this", "example": "the", "json": "function", "is": "sync"}'


@jpretty(silent=True)
async def async_json():

    return "{\"instead\": \"here\", \"is\": \"async\"}"


async def main():

    print((await to_bytesio('{"this": "is", "an_": "example", "here": 123, "even": 1.02, "but": False, "isNot": True}')).read())

    print(await prettify('{"this": "is", "an_": "example", "here": 123, "even": 1.02, "but": False}'))

    print(await prettify(b"{\"X\": 123}"))

    print(await prettify(bytearray("{\"X\": 123}", encoding='utf-8')))

    #every decorated function should be awaited (even sync)
    print((await sync_json()).read())
    print(await async_json())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## Prettifier
`prettify`: Prettifies and dumps the input (`str`, `bytes`, `bytearray`, `dict`) to json. Accepts every kwarg of `json.dumps`.
```python
await prettify('{"this": "is", "an_": "example", "here": 123, "even": 1.02, "but": False}')

await prettify(b"{\"X\": 123}")

await prettify(bytearray("{\"X\": 123}", encoding='utf-8'))

#or use the decorator

@jpretty(silent=True)
async def async_json():

    #return a json-like str, bytes, bytearray, dict and the decorator will convert it
    return "{\"instead\": \"here\", \"is\": \"async\"}"
```

## Utilities

`to_bytes`: converts input (`str`, `bytes`, `bytearray`, `dict`) to `io.BytesIO`
```python
await to_bytesio('{"this": "is", "an_": "example", "here": 123, "even": 1.02, "but": False}')

#or use the decorator

@jbytesio()
async def json_to_bytesio():

    #return a json-like str, bytes, bytearray, dict and the decorator will convert it
    return '{"in": "this", "example": "the", "json": "function", "is": "sync"}'
```

## Notes

You can use the boolean kwarg `silent` for skipping encoding exceptions.

For custom encoder use the kwarg `encoder` instead of `cls` in the function that uses the custom encoder.

Decorators can decorate both sync and async functions but always return async function that needs to be awaited.

---

Made by **nect** [@bynect](https://github.com/bynect)