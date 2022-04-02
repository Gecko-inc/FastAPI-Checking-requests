from fastapi import FastAPI
import time
import redis

app = FastAPI()


@app.get("/check")
async def check_requests(token: str, max_request_per_minutes: int):
    request_counter = redis.Redis(host='redis', port=6379, db=0)
    if request_counter.hgetall(token):
        counter = request_counter.hgetall(token)
        counter_update = dict()
        # Проверяем прошла ли минута с момента 1ого запроса из пачки
        if time.time() - float(counter.get(b'time').decode()) >= 60:
            counter_update['time'] = time.time()
            counter_update['count'] = 1
            counter_update['max_request'] = float(counter.get(b'max_request').decode())
            request_counter.hmset(token, counter_update)
            return {
                "response": True
            }
        # Проверка на превышение максимального количества запросов в минуту
        elif float(counter.get(b'count').decode()) >= float(counter.get(b'max_request').decode()):
            return {
                "response": False
            }
        counter_update['time'] = float(counter.get(b'time').decode())
        counter_update['count'] = float(counter.get(b'count').decode())
        counter_update['max_request'] = float(counter.get(b'max_request').decode())
        counter_update['count'] += 1
        request_counter.hmset(token, counter_update)

    else:
        # Если пользователь не совершал запросы, мы записываем информацию о нем в словарь
        request_counter.hmset(token, {
            "count": 1,
            "max_request": max_request_per_minutes,
            "time": time.time()
        })
    return {
        "response": True
    }
