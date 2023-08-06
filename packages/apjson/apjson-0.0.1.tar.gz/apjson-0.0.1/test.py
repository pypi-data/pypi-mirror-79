from apjson import prettify, to_bytesio, jbytesio, jpretty
import asyncio


@jbytesio(sort_keys=True, check_circular=True)
def sync_json():

    return '{"in": "this", "example": "the", "json": "function", "is": "sync"}'


@jpretty(silent=True)
async def async_json():

    return "{\"instead\": \"here\", \"is\": \"async\"}"


async def main():

    print((await to_bytesio('{"this": "is", "an_": "example", "here": 123, "even": 1.02, "but": False}')).read())

    print(await prettify('{"this": "is", "an_": "example", "here": 123, "even": 1.02, "but": False}'))

    print(await prettify(b"{\"X\": 123}"))

    print(await prettify(bytearray("{\"X\": 123}", encoding='utf-8')))

    #every decorated function should be awaited (even sync)
    print((await sync_json()).read())
    print(await async_json())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())