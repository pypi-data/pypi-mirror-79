from .base import BaseStorage, KeyError
import redis
from uliweb.utils._compat import integer_types

#connection pool format should be: (options, connection object)
__connection_pool__ = None

class Storage(BaseStorage):
    def __init__(self, cache_manager, options):
        """
        options =
            unix_socket_path = '/tmp/redis.sock'
            or
            connection_pool = {'host':'localhost', 'port':6379, 'db':0}
        """
        BaseStorage.__init__(self, cache_manager, options)

        if 'unix_socket_path' in options:
            self.client = redis.Redis(unix_socket_path=options['unix_socket_path'])
        else:
            global __connection_pool__
        
            if not __connection_pool__ or __connection_pool__[0] != options['connection_pool']:
                d = {'host':'localhost', 'port':6379}
                d.update(options['connection_pool'])
                __connection_pool__ = (d, redis.ConnectionPool(**d))
            self.client = redis.Redis(connection_pool=__connection_pool__[1])
    
    def get(self, key):
        v = self.client.get(key)
        if v is not None:
            if not v.isdigit():
                return self._load(v)
            else:
                return int(v)
        else:
            raise KeyError("Cache key [%s] not found" % key)
    
    def set(self, key, value, expiry_time):
        if not isinstance(value, integer_types):
            v = self._dump(value)
        else:
            v = value
        r = self.client.setex(name=key, value=v, time=expiry_time)
        return r
    
    def delete(self, key):
        self.client.delete(key)
        return True
        
    def inc(self, key, step, expiry_time):
        pipe = self.client.pipeline()
        r = pipe.incr(key, step).expire(key, expiry_time).execute()
        return r[0]
    
    def dec(self, key, step, expiry_time):
        pipe = self.client.pipeline()
        r = pipe.decr(key, step).expire(key, expiry_time).execute()
        return r[0]
        
        