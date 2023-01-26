from db_main import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from kafka import KafkaConsumer

response_topic = "segments"

response_message = KafkaConsumer(
    response_topic,
    bootstrap_servers = "localhost:9092"
)


engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
base.metadata.create_all(engine)


DBSession = sessionmaker(bind = engine)
session = DBSession()



