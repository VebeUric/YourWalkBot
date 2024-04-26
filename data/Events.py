import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Events(SqlAlchemyBase):
    __tablename__ = "Events"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)

    name = sqlalchemy.Column(sqlalchemy.String)
    disciption = sqlalchemy.Column(sqlalchemy.String)
    adress = sqlalchemy.Column(sqlalchemy.String)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tag = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('tags.name_tag'))

    back_tag = orm.relationship('Tag')