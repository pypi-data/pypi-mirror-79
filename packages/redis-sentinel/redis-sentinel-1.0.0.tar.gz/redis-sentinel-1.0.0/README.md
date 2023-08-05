# Python Redis Sentinel

Given a Redis + Sentinel service, this package allow you to connect simultaneously to both the master node
and to the slave nodes, transparently balancing the connection used to the user.

## Scope
The redis packages doesn't expose a tool to automatically choose between the master node and the slaves ones.
With this package, you get an object that automatically detect when to use the master one and when to connect to the slaves.

This is useful for the scenarios when you need to expose a Redis connection, you need to execute read and write operation,
but you want also take advantage of the read only nodes


## Mechanism
The automatic selection between master and slaves is detected by the Redis command executed:
into the class, there is an attribute (`REPLICAS_COMMANDS`) which contain the list of Redis' commands that will be executed on the slaves connection pool.
 
Those commands which are not listed in `REPLICAS_COMMANDS` are executed on the master node.
 
The main idea is to use the slave for the read operations (such as GET, KEYS ecc...) and to use the master just for the writes.

## Usage

Instantiate `RedisSentinel` passing a `redis.sentinel.Sentinel` instance, the service name,
and every connection parameter you would pass to the `redis.Redis` constructor (excepts obviously the host and the port, which are given by Sentinel)