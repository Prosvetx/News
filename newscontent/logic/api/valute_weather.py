import asyncio
import json
import aiohttp
from random import choice


async def start(url):
    """Асинхронный запрос с помощью aiohttp.ClientSession - результат данные в формате JSON"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            print('ok')
            return json.loads(data)


def api_weather_rates(city):
    """Получение данных о погоде, валюте с помощью OWM API и SBERBANK API в асинхронном потоке"""
    weather_token = '6e9178666ae50697fbfd35c5aa83d8f6'
    city = city
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    wth = [start(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric'),
           start('https://www.cbr-xml-daily.ru/daily_json.js')]
    res = loop.run_until_complete(asyncio.gather(*wth))
    return res


def clear_dts(api):
    """Финальная версия данных погоды и курса валют в одном словаре"""
    # отделить погоду от валют в дальнейшем
    data = {"weather": {"city": api[0]['name'], "celsius": api[0]['main']['feels_like']},
            "rates": {'USD': round(api[1]['Valute']['USD']['Value'], 2),
                      'EUR': round(api[1]['Valute']['EUR']['Value'], 2),
                      'CNY': round(api[1]['Valute']['CNY']['Value'], 2)}}
    return data
