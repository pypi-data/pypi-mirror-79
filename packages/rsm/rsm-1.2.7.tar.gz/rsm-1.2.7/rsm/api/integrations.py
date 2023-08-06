from rsm.handlers.output import LogHandler
from rsm.api.core import ApiRequest
import pandas as pd
import numpy as np
import json

if __name__ == '__main__':
	logger = LogHandler('rsm.api.integrations')
else:
	logger = LogHandler(__name__)

log = logger.logger


def integration_instances(environment, integration):
	"""
	Integration's instances for the chosen environments
	:return: instances
	"""
	try:
		if not isinstance(integration, str):
			raise TypeError(
				"Parameter: integration",
				"Wrong type: {0}".format(
					type(
						integration)))
		elif isinstance(environment, str):
			log.warning("The variable 'environment' is a string, splitting by commas")
			environment = environment.split(',')
		elif not isinstance(environment, list):
			raise TypeError(
				"Parameter: environment",
				"Wrong type: {0}".format(
					type(environment)))
		endpoint = '/external/v1/integrations/GetOptionalIntegrationInstances'
		payload = json.dumps(
			{
				"environments":
					[env for env in environment]
					if environment is not None else [""],
				"integrationIdentifier": "{0}".format(integration)
			}
		)

		result = ApiRequest().make("POST", endpoint, data=payload)

		if isinstance(result, list):
			if len(result) > 1:
				log.info(
					f"Found {len(result)} instances for environment {environment} and the '{integration}' integration")
				return result
			elif len(result) == 0:
				log.debug(f'No instances were found for environment {environment} and the {integration} integration')
				return False
		else:
			return result
	except Exception as err:
		if isinstance(err.args, tuple) and len(err.args) == 1:
			log.error(err.args[0])
		else:
			log.error(err.args)


def get_installed_integrations():
	"""
	:return Returns a dataframe containing the installed integrations.
	"""

	endpoint = '/external/v1/integrations/GetInstalledIntegrations'
	rq = ApiRequest().make('GET', endpoint)

	integrations = [integration for integration in rq]
	# actions = [action['integrationSupportedActions'] for action in integrations]
	integrations = pd.DataFrame(data=[
		np.array([key['displayName'], key['version'], key['installedVersion'],
				[action['name'] for action in key['integrationSupportedActions']],
				key['description']], dtype=object)
		for key in integrations],
		columns=['name', 'version', 'installed_version', 'actions', 'description'])
	return integrations
