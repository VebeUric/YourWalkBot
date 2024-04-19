from sqlalchemy.orm import sessionmaker

from data import db_session
from data.__all_models import *
from data.Tags import Tag
from data.Users import User
from data.Preference import Preference




class DataBaseManager:
    def __init__(self):
        db_session.global_init("db/DataBase.db")


    async def check_user(self, username):
        session = db_session.create_session()
        async with session as sess:
            async with sess.begin():
                query =  await sess.query(User).filter(User.username == username)
                session.close()
                return await query.first()



    async def add_user(self, username):
        session = db_session.create_session()
        async with session as sess:
            async with sess.begin():
                user = User()
                user.username = username
                sess.add(user)
                await sess.commit()
                session.close()



    def get_name(self, username):
        user = User()
        name = self.session.query(User).filter(User.username == username).first()
        return name

    def pass_preference(self, username, tag_id):
        preference = Preference()
        preference.useranme = username
        preference.tag_id = tag_id
        self.session.add(preference)
        self.session.commit()

    def get_all_preferences(self):
        preference = Preference()
        preferences = self.session.query(Preference).all()
        return preferences

    def get_user_preferences(self, username):
        session = db_session.create_session()
        preferences = self.session.query(Preference).filter(Preference.useranme == username).all()
        session.commit()
        return preferences

    # def get_prefereence_name_from_id(self, preference):
    #     session = db_session.create_session()


    def delete_preference(self, username, tag_id):
        preference = self.session.query(Preference).filter(Preference.useranme == username and Preference.tag_id == tag_id).first()
        if preference:
            self.session.delete(preference)
            self.session.commit()
