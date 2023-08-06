from redis import Redis, ReadOnlyError, ConnectionError, TimeoutError
from redis.sentinel import Sentinel


class _RedisSentinel(object):
    REPLICAS_COMMANDS = [
        "GET", "DUMP", "EXISTS", "MGET", "KEYS", "RANDOMKEY", "TYPE"
        "GETBIT", "GETRANGE", "STRLEN", "SUBSTR"
        "ACL GENPASS", "ACL GETUSER", "ACL LIST", "ACL USERS", "ACL WHOAMI",
        "LINDEX", "LLEN", "LRANGE"
    ]

    def __init__(self, sentinel: Sentinel, service_name: str, REPLICAS_COMMANDS: [str] = None, **kwargs):
        self.master: Redis
        self.slave: Redis

        self.sentinel: Sentinel = sentinel
        self.service_name: str = service_name

        if REPLICAS_COMMANDS is not None:
            self.REPLICAS_COMMANDS = REPLICAS_COMMANDS

        self.config = kwargs
        self.connect()

    def connect(self):
        self.master = self.sentinel.master_for(service_name=self.service_name, **self.config)
        self.slave = self.sentinel.slave_for(service_name=self.service_name, **self.config)

    def close(self):
        self.master.close()
        self.slave.close()

    def execute_command(self, *args, no_redis_sentinel_retry=False, **options):
        command_name = args[0]
        try:
            if command_name in self.REPLICAS_COMMANDS:
                return self.slave.execute_command(*args, **options)
            else:
                return self.master.execute_command(*args, **options)
        except (ConnectionError, TimeoutError, ReadOnlyError) as e:
            if no_redis_sentinel_retry:
                raise e
            self.connect()
            return self.execute_command(*args, no_redis_sentinel_retry=True, **options)

    def get_master(self) -> Redis:
        return self.master

    def get_slave(self) -> Redis:
        return self.slave


RedisSentinel = type("RedisSentinel", (_RedisSentinel, Redis), {})
