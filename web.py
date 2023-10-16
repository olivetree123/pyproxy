from sanic import Sanic
from sanic.response import text

app = Sanic("MyHelloWorldApp")


@app.middleware("request")
async def extract_user(request):
    print("接收到请求...")


@app.get("/")
async def hello_world(request):
    return text("Hello")
