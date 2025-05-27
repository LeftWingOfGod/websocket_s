import asyncio
import hmac
import hashlib
import base64
from aiohttp import ClientSession, WSMsgType

API_KEY = "VALID_API_KEY"
CLIENT_SECRET = "3a8e5f1b-9c2d-4e7f-a6b0-5d3c1f8e4a9d"
WS_URL = "ws://localhost:8080/ws"

def generate_signature():
    signature_string = (
        "(request-target): get /ws\n"
        "authority: localhost:8080"
    )
    digest = hmac.new(
        CLIENT_SECRET.encode(),
        signature_string.encode(),
        hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode()

async def websocket_client():
    signature = generate_signature()
    
    headers = {
        "X-API-KEY": API_KEY,
        "Signature": f'headers="(request-target) authority", '
                    f'algorithm="hmac-sha256", '
                    f'signature="{signature}"',
        "Host": "localhost:8080"
    }

    async with ClientSession() as session:
        try:
            async with session.ws_connect(WS_URL, headers=headers) as ws:
                print("连接成功")
                await ws.send_str("Hello Server!")
                async for msg in ws:
                    if msg.type == WSMsgType.TEXT:
                        print(f"收到响应: {msg.data}")
                        break
        except Exception as e:
            print(f"失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(websocket_client())