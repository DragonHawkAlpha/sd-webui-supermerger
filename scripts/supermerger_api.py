'''
API for Super Merger - Stable Diffusion Web UI extension for super merges.
Api logic is in api\SuperMergerApi
Examples taken from ilian.iliev's EyeMask extension.

Author: DragonHawkAlpha
Since: 11.05.2024
'''

import os
import sys

from modules import scripts
sys.path.append(os.path.join(scripts.basedir(), 'scripts'))

import modules.script_callbacks as script_callbacks
from supermergerapi.api import SuperMergerApi

try:
    api = SuperMergerApi()
    script_callbacks.on_app_started(api.start)
except:
    pass