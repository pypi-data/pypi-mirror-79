import logging
import os

from nexuscli.nexus_config import NexusConfig
from nexuscli.nexus_client import NexusClient

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING').upper()

ROOT_LOGGER = logging.getLogger(__name__)
ROOT_LOGGER.setLevel(LOG_LEVEL)
ROOT_LOGGER.addHandler(logging.NullHandler())

__all__ = ['NexusConfig', 'NexusClient']
