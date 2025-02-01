from connectors.redis_connector import RedisManager
from conf import SETTINGS


redis_manager = RedisManager(
    host=SETTINGS.REDIS_HOST,
    port=SETTINGS.REDIS_PORT,
)
