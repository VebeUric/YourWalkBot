import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Wishlist(SqlAlchemyBase):
    __tablename__ = "Wishlist"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)

    event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Events.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    event_back = orm.relationship("Event", back_populates="wishlist_back")
    user_back = orm.relationship('User', back_populates="wishlist_back")