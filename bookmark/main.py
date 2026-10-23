# async def app(scope, receive, send):
#     assert scope['type'] == 'http'

#     await send({
#         'type': 'http.response.start',
#         'status': 200,
#         'headers': [
#             (b'content-type', b'text/plain'),
#             (b'content-length', b'13'),
#         ],
#     })
#     await send({
#         'type': 'http.response.body',
#         'body': b'Hello, world!',
#     })

# uvicorn main:app

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# pip run fastapi dev