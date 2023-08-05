


# hwhpykit

- 依据个人习惯封装的常用第三方库
- 依赖的第三方库：
  - [Redis](https://github.com/andymccurdy/redis-py) 

## Main function

- Cache
> Redis-client 

- Buffer
> Kafka-client

- DataBase
> MySQL-client
> PostgreSQL-client


## Cache

### Redis-client

RedisManager.config(host="127.0.0.1", db=0)
RedisManager.string.set("reids", "value")
RedisManager.string.set_keys({"a":1, "b": 2})
RedisManager.string.set_range("redis", 6, "666")
RedisManager.string.set_not_exist_key('11', "1222")


RedisManager.string.append('redis', '---')

key = 'redis'
r = RedisManager.string.get(key)
print(r)

r = RedisManager.string.get_len(key)
print(r)

r = RedisManager.string.get_range(key, 0, -1)
print(r)

r = RedisManager.string.get_values(['11', "1222"])
print(r)

RedisManager.string.set('2', '0')
RedisManager.string.increase('2')
RedisManager.string.increase('2', -100000)
r = RedisManager.string.get('2')
print(r)


### Database



