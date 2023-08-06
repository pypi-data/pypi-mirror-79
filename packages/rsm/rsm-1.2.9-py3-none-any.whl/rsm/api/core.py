from rsm.handlers.output import LogHandler
from rsm.override.rsmsdk import RsmSDK
import urllib3
import json

urllib3.disable_warnings()

# from SiemplifyDataModel import CyberCase, AlertInfo

log = LogHandler(__name__)

try:
	from Siemplify import Siemplify  # E402

except ModuleNotFoundError as err:
	from rsm.mocking.Siemplify import Siemplify
	log.warning("Importing mocking module `Siemplify` since the original module was not found.")
	pass
except ImportError as err:
	log.error(err)


class ApiRequest(Siemplify):
	def __init__(self):
		self.sdk_config = RsmSDK()
		super(ApiRequest, self).__init__()

	def make(self, method, endpoint, **kwargs):
		self.API_ROOT = "https://127.0.0.1/api"
		log.info(f'API_ROOT set to: {self.API_ROOT}')
		url = self.API_ROOT + endpoint
		headers = self.session.headers
		raw_data = None

		if method in ("POST", "GET"):
			if "Content-Type" not in headers:
				headers["Content-Type"] = "application/json"
				raw_data = kwargs.pop("data", {})
				raw_data = json.dumps(raw_data, sort_keys=True)
		try:
			result = self.session.request(
				method, url, raw_data, headers=headers, **kwargs)
			# if result.headers.get('Transfer-Encoding') and result.headers.get('Transfer-Encoding') == 'chunked':
			#     # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding
			#     result = result.text
			# else:
			result = result.json()
		except Exception as err:
			return err

		return result
