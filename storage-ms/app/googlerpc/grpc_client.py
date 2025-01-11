# Author: Nina Mislej
# Date created: 5.12.2024

# GRPC Logic.
import asyncio
from proto import code_ms_pb2_grpc
from proto import code_ms_pb2
import grpc

async def run(item_code : str) -> None:
    async with grpc.aio.insecure_channel("localhost:8010") as channel:
        stub = code_ms_pb2_grpc.CodeServiceStub(channel)
        response = await stub.CreateCode(code_ms_pb2.CodeRequest(item_code=item_code))
    print("Image received: " + response.image_base64)

#class CodeClient(object):
#
#    def __init__(self):
#        self.host = 'localhost'
#        self.server_port = 8010
#
#        # Instantiate a channel.
#        self.channel = grpc.insecure_channel(f"{self.host}:{self.server_port}")
#
#        # Bind the client and the server.
#        self.stub = code_ms_pb2_grpc.CodeServiceStub(self.channel)
#
#    def get_url(self, item_code):
#        code = code_ms_pb2.CodeRequest(item_code=item_code)
#        return self.stub.CreateCode(code)

if __name__ == '__main__':
    result = asyncio.run(run("Test"))