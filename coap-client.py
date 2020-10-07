import logging
import asyncio
import sys
from aiocoap import *

logging.basicConfig(level=logging.INFO)

rqType = sys.argv[2]

async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = b"The quick brown fox jumps over the lazy dog.\n" * 30
    if rqType == "time":
        request = Message(code=GET, uri="coap://{}/time".format(sys.argv[1]))

    if rqType == "block-get":
        request = Message(code=GET, payload=payload,uri="coap://{}/other/block".format(sys.argv[1]))

    if rqType == "block-put":
        request = Message(code=PUT, payload=payload, uri="coap://{}/other/block".format(sys.argv[1]))

    if rqType == "separate":
        request = Message(code=GET, uri="coap://{}/other/separate".format(sys.argv[1]))


    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())