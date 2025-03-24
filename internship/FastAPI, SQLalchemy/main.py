# Импортируем нужные инструменты
from fastapi import FastAPI

# Создаём "коробку" для нашего приложения (как коробка для игрушек)
app = FastAPI()

# Говорим: "Когда кто-то заходит на главную страницу, покажи приветствие"
@app.get("/")  # "/" = главная страница сайта
def home():
    return {"message": "Привет! Это мой первый сайт!"}

# Делаем страницу для получения информации о пользователе
@app.get("/user/{user_id}")  # {user_id} — как номер квартиры в адресе
def get_user(user_id: int):  # user_id должен быть цифрой (int)
    return {
        "user_id": user_id,
        "name": "Вася Пупкин",
        "email": "vasya@example.com"
    }

# Страница для отправки сообщений (как форма обратной связи)
@app.post("/send-message")
def send_message(message: str):  # message — текст сообщения
    return {
        "status": "Сообщение доставлено!",
        "your_message": message
    }
