from sqlalchemy.orm import sessionmaker

from data import db_session
from data.__all_models import *
from data.Tags import Tag
from data.Users import User
from data.Preference import Preference
from data.Events import Event
from data.WishList import Wishlist



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


    def get_id_from_username(self, usrname):
        id = None
        if usrname:
            id = self.session.query(User).filter(User.username == usrname).first().id
        return id
    def get_decription(self, link):
        with open(str(link), 'r', encoding="utf-8") as file:
             text = file.read()
             return text
    def get_name(self, username):
        user = User()
        name = self.session.query(User).filter(User.username == username).first()
        return name

    def check_in_wishlist(self, event_id, user_id):
        event = self.session.query(Wishlist).filter(Wishlist.event == event_id and Wishlist.user == user_id).first()
        return event

    def get_my_events(self, user_id):
        my_events = []
        my_events_id = self.session.query(Wishlist).filter(Wishlist.user == user_id).all()
        print(my_events_id)
        for event in my_events_id:
            print(event.id)
            res = self.session.query(Event).filter(Event.id == event.event).first()
            my_events.append(res)
        print(my_events)
        return my_events
    def add_to_wishlist(self, event_id, user_id):
        print(user_id)
        wishlist = Wishlist()
        wishlist.event = event_id
        wishlist.user = user_id
        self.session.add(wishlist)
        self.session.commit()


    def delete_from_wishlist(self, user_id, event_id):
       print(890174087894)
       event = self.session.query(Wishlist).filter(Wishlist.user == user_id and Wishlist.event == event_id).first()
       self.session.delete(event)
       self.session.commit()


    def get_events(self, tags):
        res = []
        if tags:
            if len(tags) > 1:
                for tag in tags:
                    neded_tag_id = self.session.query(Tag).filter(Tag.name_tag == tag).first().id
                    events = self.session.query(Event).filter(Event.tag_id == neded_tag_id).all()
                    res.append(*events)
                print([i.name for i in res])
                return res
            else:
                print(44444444444444444444444444)
                tag_id_new = self.session.query(Tag).filter(Tag.name_tag == tags[0]).first().id
                print(tag_id_new)
                print(Event.name, tags[0])
                neded_tag_id = self.session.query(Tag).filter(Tag.name_tag == tags[0]).first().id
                events = self.session.query(Event).filter(Event.tag_id == neded_tag_id).all()
                return events
        else:
            events = self.session.query(Events).all()
            return events
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

