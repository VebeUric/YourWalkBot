import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)

    preference = orm.relationship("Preference", back_populates="user")
    wishlist_back = orm.relationship("Wishlist", back_populates="user_back")
