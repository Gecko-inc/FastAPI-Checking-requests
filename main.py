from fastapi import FastAPI
import time

# Наш словарь с данными пользователей
request_counter = dict()

app = FastAPI()


@app.get("/check")
async def check_requests(token: str, max_request_per_minutes: int):
    if request_counter.get(token):
        # Проверяем прошла ли минута с момента 1ого запроса из пачки
        counter = request_counter.get(token)
        if time.time() - counter.get('time') >= 60:
            counter['time'] = time.time()
            counter['count'] = 0
        # Проверка на превышение максимального количества запросов в минуту
        if counter['count'] >= counter['max_request']:
            return {
                "response": False
            }
        counter['count'] += 1

    else:
        # Если пользователь не совершал запросы, мы записываем информацию о нем в словарь
        request_counter[token] = {
            "count": 1,
            "max_request": max_request_per_minutes,
            "time": time.time()
        }
    return {
        "response": True
    }
