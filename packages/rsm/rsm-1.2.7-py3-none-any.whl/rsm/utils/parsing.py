from rsm.handlers.output import LogHandler
import rsm.api.integrations

log = LogHandler(__name__)


class ParseIntegrations:
	def __init__(self):
		self.integrations = rsm.api.integrations.get_installed_integrations()

	def parsed_installed_integration(self):
		"""
		# TODO: include the description of each action (tuple)
		:return: JSON results containing the Integration, Actions and Description
		"""
		integrations = self.integrations
		result = {}
		for integration in integrations.name.tolist():
			selected = integrations[integrations['name'] == integration]
			if integration not in result.keys():
				result.update({integration: {}})
			integrations.explode('actions').dropna(subset=['actions'])
			result[integration] = {
				"Actions": selected.explode('actions')['actions'].dropna().tolist(),
				"Description": selected.description.max(),

				# The parameters below are commented since the API endpoint use for this request does not return
				# "InstalledVersion", "hasConnector" and many other fields properly.
				# TODO: change for this endpoint: /v1/store/GetIntegrationsStoreData
				# "Version": selected.version.max(),
				# "InstalledVersion": selected.installed_version.max()
			}
		return result

	def get_installed_integration_actions(self, name):
		"""

		:param name: Integration name
		:return: Dataframe containing all the available actions of the chosen integration.
		"""
		df = self.integrations
		return df['actions'][df['name'] == name].explode('actions')



