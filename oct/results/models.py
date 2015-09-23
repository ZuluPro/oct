from peewee import Proxy, TextField, FloatField, CharField, SqliteDatabase, Model

db = Proxy()


class Result(Model):
    error = TextField(null=True)
    scriptrun_time = FloatField()
    elapsed = FloatField()
    epoch = FloatField()
    custom_timers = TextField(null=True)
    turret_name = CharField(default='Noname')

    class Meta:
        database = db


def set_database(db_path, proxy):
    database = SqliteDatabase(db_path, check_same_thread=False)
    proxy.initialize(database)
