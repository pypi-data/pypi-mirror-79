import getopt, sys
from rsm.override.rsmsdk import RsmSDK as SiemplifySdkConfig


class SiemplifyBase:

	def __init__(self):
		def __init__(self):
			self.sdk_config = SiemplifySdkConfig()
			self.RUN_FOLDER = self.sdk_config.run_folder_path
			self.script_name = ""
			self._logger = None
			self._logs_collector = None
			self._log_path = None
			self._log_use_elastic = False
			options, _ = getopt.gnu_getopt(sys.argv[1:], "", ["useElastic", "logPath="])

			for name, value in options:
				if name == "--logPath":
					self._log_path = value.strip('"')
				elif name == "--useElastic":
					self._log_use_elastic = True

