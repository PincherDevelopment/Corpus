import logging
from config import CONFIG

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger("corpus")

logger.info("Initializing Corpus...")

generator = CONFIG["DEFAULT"]["generator"]
logger.info("Used generator: %s" % generator)
used_generator = __import__("generators.%s" % generator, fromlist=["generators"])

from personality_engine import set_generator
set_generator(used_generator)

bridge = CONFIG["DEFAULT"]["bridge"]
logger.info("Used bridge: %s" % bridge)
globals()["used_bridge"] = __import__("bridges.%s" % bridge, fromlist=["bridges"])
