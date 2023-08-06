from sqlalchemy.orm import relation

from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Index


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)

    site_id = Column(Integer, ForeignKey('site.id', ondelete='CASCADE'))
    site = relation('Site', back_populates="news")

    name = Column(String(32), nullable=False)
