from sqlalchemy.orm import relation

from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Index


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)

    name = Column(String(32), nullable=False)
