from datetime import datetime
from peewee import *

from database import *


class DatingRequest(Model):
    request_id = CharField(primary_key=True)
    form_data = TextField(default='')
    form_type = CharField(default='')
    data_type = CharField(default='')
    are_files_downloaded = BooleanField(default=False)
    time_created = TimestampField(default=datetime.now())
    time_processed = TimestampField()
    is_processed = BooleanField(default=False)
    is_uploaded = BooleanField(default=False)

    class Meta:
        database = db

    def set_are_files_downloaded(self, are_files_downloaded=False):
        self.are_files_downloaded = are_files_downloaded
        self.save()

    def set_time_processed(self, timestamp):
        self.time_processed = timestamp
        self.save()


    def set_is_processed(self, is_processed=False):
        self.is_processed=is_processed
        self.save()

    def set_is_uploaded(self, is_uploaded=False):
        self.is_uploaded = is_uploaded
        self.save()

    datingrequest_attr = ['request_id', 'form_data', 'form_type', 'data_type',
                          'are_files_downloaded', 'time_created', 'time_processed',
                          'is_processed', 'is_uploaded']

