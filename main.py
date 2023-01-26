import json
import time
from kafka import KafkaProducer, producer
import numpy as np

monetary_topic = "monetary"
recency_topic = "recency"
frequency_topic = "frequency"

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
              api_version=(0,11,5)
                         )
print("Values are generated for each minutes")



while True:
    monetary_dict = {}
    recency_dict = {}
    frequency_dict = {}

    monetary_dict["monetary"] = [float(i) for i in np.random.randint(0, 1000, 100)]
    recency_dict["recency"] = [float(i) for i in np.random.randint(0, 366, 100)]
    frequency_dict["frequency"] = [float(i) for i in np.random.randint(0, 366, 100)]


    producer.send(
        monetary_topic,
        json.dumps(monetary_dict).encode("utf-8")
    )
    producer.send(
        recency_topic,
        json.dumps(recency_dict).encode("utf-8")
    )
    producer.send(
        frequency_topic,
        json.dumps(frequency_dict).encode("utf-8")
    )
    print("Done Sending...")
    time.sleep(60)
    continue


