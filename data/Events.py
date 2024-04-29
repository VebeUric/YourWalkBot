import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase):
    __tablename__ = "Events"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)

    name = sqlalchemy.Column(sqlalchemy.String)
    disciption = sqlalchemy.Column(sqlalchemy.String)
    adress = sqlalchemy.Column(sqlalchemy.String)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tags.id'))
    photo_link = sqlalchemy.Column(sqlalchemy.String)

    wishlist_back = orm.relationship("Wishlist", back_populates="event_back")
    back_tag = orm.relationship('Tag', back_populates="event_tag")