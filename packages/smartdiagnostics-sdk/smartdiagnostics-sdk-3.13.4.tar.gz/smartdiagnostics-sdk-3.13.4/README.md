# SMARTdiagnostics SDK

Python SDK to enable users to more easily integrate with the SMARTdiagnostics API.

# Code Sample

``` python
from smartdiagnostics_sdk import SmartDiagnosticsApi, models
import configparser

# Get configuration
configuration = configparser.ConfigParser()
configuration.read("settings.ini")

# Prod base_url example: https://sd.kcftech.com
base_url = configuration["SDAPI"]["base_url"]
bearer_token = configuration["SDAPI"]["token"]

# instantiate client and add token for requests
sd_client = SmartDiagnosticsApi(base_url=base_url)
sd_client.config.headers["Authorization"] = "bearer " + bearer_token

assets_response = sd_client.get_assets()

# print details for each asset
for asset in assets_response.result:
    details = sd_client.get_asset_details(asset.id)
    print(details)
```