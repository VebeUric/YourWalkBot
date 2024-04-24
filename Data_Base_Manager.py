from sqlalchemy.orm import sessionmaker

from data import db_session
from data.__all_models import *
from data.Tags import Tag
from data.Users import User
from data.Preference import Preference




class DataBaseManager:
    def __init__(self):
        db_session.global_init("db/DataBase.db")
        self.session = db_session.create_session()


    def check_user(self, username):
        session = db_session.create_session()
        print(type(session))
        query = self.session.query(User).filter(User.username == username)
        return query.first()



    def add_user(self, username):
       session = db_session.create_session()
       user = User()
       user.username = username
       self.session.add(user)
       self.session.commit()
       self.session.close()



    def get_name(self, username):
        user = User()
        name = self.session.query(User).filter(User.username == username).first()
        return name


    def get_tag_id_from_name(self, tagname):
       tag_id = self.session.query(Tag).filter(Tag.name_tag == tagname).first()
       return tag_id.id

    def pass_preference(self, username, tag_id):
        preference = Preference()
        preference.useranme = username
        preference.tag_id = tag_id
        self.session.add(preference)
        self.session.commit()

    def get_all_preferences(self):
        preferences = [tag.name_tag for tag in self.session.query(Tag).all()]
        print(preferences)
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
