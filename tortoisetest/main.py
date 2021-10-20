import time
from starlette.requests import Request

import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.responses import Response
from tortoise import Tortoise
from models.UserModel import Account
import aioredis


app = FastAPI()


@app.get('/index')
async def index(response: Response):
    t = time.time()
    account = Account(name=f'asdsd{t}')
    await account.save()
    response.set_cookie('username', 'zhansan')
    return {'msg': 'hello world'}


@app.get('/query')
async def accout_list_get():
    name = await Account.all().values('name')
    return {'data': name}


async def db_init():
    user = 'root'
    password = 'root'
    db_name = 'mytest'
    await Tortoise.init(
        db_url=f'mysql://{user}:{password}@127.0.0.1:3306/{db_name}',
        # 这里models是自己定义的models
        modules={'models': ['models.UserModel']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


@app.get('/query_redis_key')
async def query_redis_key(key: str, request: Request):
    val = await request.app.state.redis.get(key)

    return {'data': val}


async def redis_init(app: FastAPI):
    conn = await aioredis.create_redis_pool(
        'redis://127.0.0.1/0')
    app.state.redis = conn
    val = await conn.execute('GET', 'my_key')
    await conn.expire('my_key', 30)
    print(val)
    return val


@app.on_event('startup')
async def start_up():
    await db_init()
    await redis_init(app)


@app.on_event('shutdown')
async def shut_down():
    app.state.redis.close()


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True, debug=True)
