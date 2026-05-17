from sqlalchemy import Column, Integer, String
from database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    log_text = Column(String)
    incident_type = Column(String)
    severity = Column(String)
    status = Column(String, default="open")