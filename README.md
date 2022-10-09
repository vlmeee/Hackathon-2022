# Hackathon-2022
Track DATA

## Инструкция по запуску api
Использовался Linux

Должен быть установлен и запущен Redis (запускалось на версии 5.0.7)

1. Для запуска нужна версия python 3.10.
2. Создаем виртуальное окружение в директории Hackathon-2022/stratagems и активируем его
```
python3 -m venv venv
source venv/source .env/bin/activate
```
3. Из директории Hackathon-2022/stratagems : 
```
pip3 install -r requirements.txt
```
3. Из директории Hackathon-2022/stratagems выполнить в терминале: 
```
python3 manage.py runserver
```
4. Открыть http://127.0.0.1:8000.
5. Запускаем Celery(каждая в новой вкладке терминала)
```
celery -A stratagems beat -l info
```
```
celery -A stratagems worker -l INFO
```
6. Для запуска бота нам потребуется API Token бота, его можно получить при создании у https://t.me/BotFather
7. В файле stratagems/telegram_bot/telegram_bot.py заменяем строку и подставляем выданный BotFather token
```
bot = telebot.TeleBot(<Ваш токен>)
```
8. Запускаем бота в новой вкладке терминала
```
python3 telegram_bot/telegram_bot.py 
```
## Точки входа API
http://127.0.0.1:8000/news/director/<br/>
http://127.0.0.1:8000/news/buh/
