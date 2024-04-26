import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Tag(SqlAlchemyBase):
    __tablename__ = 'tags'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_tag = sqlalchemy.Column(sqlalchemy.String)

    prefernce_tag = orm.relationship("Preference", back_populates="tag")
    event_tag = orm.relationship("Events", back_populates="back_tag")