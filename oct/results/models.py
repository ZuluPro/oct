import json
import datetime
from playhouse.pool import PooledDatabase
from peewee import Proxy, TextField, FloatField, CharField, IntegerField, Model, DateTimeField, SqliteDatabase

db = Proxy()


# Temporary, waiting new peewee release
class PooledSqliteDatabase(PooledDatabase, SqliteDatabase):
    def _is_closed(self, key, conn):
        closed = super(PooledSqliteDatabase, self)._is_closed(key, conn)
        if not closed:
            try:
                conn.total_changes
            except:
                return True
        return closed


class Result(Model):
    """Define a result model
    """
    error = TextField(null=True)
    scriptrun_time = FloatField()
    elapsed = FloatField()
    epoch = FloatField()
    custom_timers = TextField(null=True)
    turret_name = CharField(default='Noname')

    def to_dict(self):
        return {
            'error': self.error,
            'scriptrun_time': self.scriptrun_time,
            'elapsed': self.elapsed,
            'epoch': self.epoch,
            'custom_timers': json.loads(self.custom_timers),
            'turret_name': self.turret_name
        }

    class Meta:
        database = db


class Turret(Model):
    """Define a turret model
    """
    name = TextField()
    uuid = TextField()
    cannons = IntegerField()
    script = TextField()
    rampup = IntegerField()
    status = TextField()
    updated_at = DateTimeField(default=datetime.datetime.now())

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Turret, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            'name': self.name,
            'uuid': self.uuid,
            'cannons': self.cannons,
            'script': self.script,
            'rampup': self.rampup,
            'status': self.status,
            'updated_at': self.updated_at
        }

    class Meta:
        database = db


def set_database(db_path, proxy, config):
    """Initialize the peewee database with the given configuration

    :param str db_path: the path of the sqlite database
    :param peewee.Proxy proxy: the peewee proxy to initialise
    :param dict config: the configuration dictionnary
    """
    pooling_params = {
        'max_connections': config.get('worker_threads', 16),
        'stale_timeout': 300
    }
    if 'testing' in config and config['testing'] is True:
        database = PooledSqliteDatabase('/tmp/results.sqlite', check_same_thread=False, **pooling_params)
    else:
        database = PooledSqliteDatabase(db_path, check_same_thread=False, **pooling_params)
    proxy.initialize(database)
