from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, ForeignKey


class NewsTag(Base):
    __tablename__ = 'news_tag'

    id = Column(Integer, primary_key=True)

    news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"))
    tag_id = Column(Integer, ForeignKey("tag.id", ondelete="CASCADE"))
