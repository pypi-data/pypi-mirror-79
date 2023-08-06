from sqlalchemy.orm import relation

from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Index


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)

    name = Column(String(32), nullable=False)

    parent_tag_id = Column(Integer, ForeignKey('tag.id', ondelete='CASCADE'))

    parent_tag = relation("Tag", foreign_keys="Tag.parent_tag_id", back_populates='children_tags')

    children_tags = relation("Tag")
