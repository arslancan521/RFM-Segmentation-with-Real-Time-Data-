from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine



base = declarative_base()

class Segments(base):
  __tablename__ = "RFM Segments"
  id = Column(Integer, primary_key = True)
  monetary_score = Column(Numeric)
  recency_score = Column(Numeric)
  frequency_score = Column(Numeric)
  segment = Column(String)
  



engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
base.metadata.create_all(engine)
