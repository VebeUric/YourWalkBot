import sqlalchemy
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase


class Preference(SqlAlchemyBase):
    __tablename__ = "preference"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    useranme = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.username'))
    tag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tags.id'))

    user = orm.relationship('User')
    tag = orm.relationship('Tag')