import json

import pandas as pd
from kafka import KafkaConsumer
from kafka import KafkaProducer
from db_main import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

monetary_topic = "monetary"
recency_topic = "recency"
frequency_topic = "frequency"
response_topic = "segments"

monetary_value = KafkaConsumer(
    monetary_topic,
    bootstrap_servers = "localhost:9092"
)
recency_value = KafkaConsumer(
    recency_topic,
    bootstrap_servers = "localhost:9092"
)
frequency_value = KafkaConsumer(
    frequency_topic,
    bootstrap_servers = "localhost:9092"
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092']
)
print("Gonna start listening...")

values_dict = {}



while True:

    for message, message1, message2 in zip(monetary_value, recency_value, frequency_value):
        temp_message = json.loads(message.value.decode())
        values_dict["Monetary"]= temp_message["monetary"]

        hum_message = json.loads(message1.value.decode())
        values_dict["Recency"] = hum_message["recency"]

        oxy_message = json.loads(message2.value.decode())
        values_dict["Frequency"] = oxy_message["frequency"]

        print(values_dict)

        df = pd.DataFrame(values_dict)
        df["RecencyScore"] = pd.qcut(df["Recency"], 5, labels=[5, 4, 3, 2, 1])
        df["FrequencyScore"] = pd.qcut(df["Frequency"], 5, labels=[1, 2, 3, 4, 5])
        df["MonetaryScore"] = pd.qcut(df["Monetary"], 5, labels=[1, 2, 3, 4, 5])
        df["RFM_Scores"] = df["RecencyScore"].astype(str) + df["FrequencyScore"].astype(str) + df[
            "MonetaryScore"].astype(str)
        seg_map = {
            r'[1-2][1-2]': 'Hibernating',
            r'[1-2][3-4]': 'At_Risk',
            r'[1-2]5': 'Cant_Loose',
            r'3[1-2]': 'About_to_Sleep',
            r'33': 'Need_Attention',
            r'[3-4][4-5]': 'Loyal_Customers',
            r'41': 'Promising',
            r'51': 'New_Customers',
            r'[4-5][2-3]': 'Potential_Loyalists',
            r'5[4-5]': 'Champions'
        }
        df["Segment"] = df["RecencyScore"].astype(str) + df["FrequencyScore"].astype(str)

        df["Segment"] = df["Segment"].replace(seg_map, regex=True)

        engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
        base.metadata.create_all(engine)

        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        for i in range(100):
            x = Segments(monetary_score = int(df["MonetaryScore"].loc[i]), recency_score = int(df["RecencyScore"].loc[i]),
                     frequency_score = int(df["FrequencyScore"].loc[i]), segment = str(df["Segment"].loc[i]))

            session.add(x)
            session.commit()





