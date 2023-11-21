from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import asyncio
import aio_pika
from aiohttp import ClientSession
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uvicorn

app = FastAPI()

# Соединение с SQL БД
engine = create_engine('sqlite:///result.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Модель для хранения результатов в БД
class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    title = Column(String)
    x_avg_count_in_line = Column(Float)

Base.metadata.create_all(engine)

# Модель для входных данных
class InputData(BaseModel):
    datetime: str
    title: str
    text: str

# Модель для результата
class OutputData(BaseModel):
    datetime: str
    title: str
    x_avg_count_in_line: float

# Функция для вычисления количества вхождений буквы "Х" в строке
def compute_x_count(text: str) -> int:
    return text.lower().count('х')

# Функция для отправки данных в брокер сообщений
async def send_data_to_broker(data: dict):
    connection = await aio_pika.connect_robust("amqp://admin:admin@rabbitmq:5672/")
    channel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(body=str(data).encode()),
        routing_key="data_queue"
    )

    await connection.close()

# Загрузка данных в БД
def save_data_to_db(data: dict):
    session = Session()
    result = Result(datetime=datetime.datetime.strptime(data['datetime'], '%d.%m.%Y %H:%M:%S.%f'),
                    title=data['title'],
                    x_avg_count_in_line=data['x_avg_count_in_line'])
    session.add(result)
    session.commit()

# Асинхронная функция для обработки данных
async def process_data(data: dict):
    x_count = compute_x_count(data['text'])
    x_avg_count = x_count / len(data['text'])
    data['x_avg_count_in_line'] = round(x_avg_count, 3)
    await send_data_to_broker(data)
    save_data_to_db(data)

# Эндпоинт для загрузки данных
@app.post("/upload_data")
async def upload_data(data: InputData):
    await asyncio.sleep(3)
    await process_data(data.dict())
    return {"message": "Data uploaded"}

# Эндпоинт для получения результата из БД
@app.get("/result")
def get_result():
    session = Session()
    results = session.query(Result).all()
    output_data = []
    for result in results:
        output_data.append(OutputData(datetime=result.datetime.strftime('%d.%m.%Y %H:%M:%S.%f'),
                                      title=result.title,
                                      x_avg_count_in_line=result.x_avg_count_in_line))
    return output_data

# Функция для запуска приложения
def run_app():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Запуск приложения при выполнении скрипта
if __name__ == "__main__":
    run_app()
