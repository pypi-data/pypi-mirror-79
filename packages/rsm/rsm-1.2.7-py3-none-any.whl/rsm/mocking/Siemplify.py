import os
import re
import json
import requests

from rsm.override.rsmsdk import RsmSDK
from rsm.mocking.ScriptResult import ScriptResult
from rsm.mocking.SiemplifyBase import SiemplifyBase

REGEX_CONFIGURATION = r"(?<=\[)[^[\]\:]*:::[^[\]]*(?=])"
EXTERNAL_CONFIG_PROVIDER_FILE = r"external_providers.json"
INSIGHT_DEFAULT_THREAT_SOURCE = "Siemplify System"
REMOTE_INTEGRATION_FILE = 'integration_conf.json'
EXTERNAL_PROVIDER_SEPARATOR = ":::"
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}


class Siemplify(SiemplifyBase):
    def __init__(self):
        super(Siemplify, self).__init__()
        self.api_key = os.environ["AppKey"]  # original: self.api_key = sys.argv[1]
        self._result = ScriptResult([])
        self.API_ROOT = self.sdk_config.api_root_uri
        self.is_remote = self.sdk_config.is_remote_publisher_sdk

        if not self.is_remote:
            # Create regular Session
            self.session = requests.Session()
            self.session.verify = False
            HEADERS.update({"AppKey": self.api_key})
            self.session.headers.update(HEADERS)