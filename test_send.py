

import asyncio
import websockets


image = 't2.jpeg'
async def send_frames(websocket):
    with open(image, 'rb') as file:
        image_bytes = file.read()
        await websocket.send(image_bytes)


async def hello():
	async with websockets.connect('ws://85.120.206.111:8001/ws') as websocket:
		while True:
			await send_frames(websocket)
			response = await websocket.recv()
			print(response)


asyncio.get_event_loop().run_until_complete(hello())
