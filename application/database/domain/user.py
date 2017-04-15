from peewee import *

from database import *


class User(Model):
    user_id = CharField(primary_key=True)
    family_name = TextField(default='')
    given_name = TextField(default='')
    email = TextField(default='')
    gender = CharField(default='')
    link = TextField(default='')
    locale = TextField(default='')
    name = TextField(default='')
    picture = TextField(default='')
    verified_email = BooleanField(default=False)
    credentials = TextField(default='')

    class Meta:
        database = db

    def save_user_info(self, user_info):

        if 'family_name' in user_info and user_info['family_name'] != None:
            self.family_name = user_info['family_name']

        if 'given_name' in user_info and user_info['given_name'] != None:
            self.given_name = user_info['given_name']

        if 'email' in user_info and user_info['email'] != None:
            self.email = user_info['email']

        if 'gender' in user_info and user_info['gender'] != None:
            self.gender = user_info['gender']

        if 'link' in user_info and user_info['link'] != None:
            self.link = user_info['link']

        if 'locale' in user_info and user_info['locale'] != None:
            self.locale = user_info['locale']

        if 'name' in user_info and user_info['name'] != None:
            self.name = user_info['name']

        if 'picture' in user_info and user_info['picture'] != None:
            self.picture = user_info['picture']

        if 'verified_email' in user_info and user_info['verified_email'] != None:
            self.verified_email = user_info['verified_email']

        if 'credentials' in user_info and user_info['credentials'] != None:
            self.credentials = user_info['credentials']

        self.save()

    def update_credentials(self, credentials):
        self.credentials = credentials
        self.save()

    user_attr = ['user_id', 'family_name', 'given_name', 'email',
                 'gender', 'link', 'locale', 'name', 'picture',
                 'verified_email', 'credentials']
