# AVEVA Data Hub Assets Python Sample

| :loudspeaker: **Notice**: Samples have been updated to reflect that they work on AVEVA Data Hub. The samples also work on OSIsoft Cloud Services unless otherwise noted. |
| -----------------------------------------------------------------------------------------------|  

**Version:** 1.1.0

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/ADH/aveva.sample-adh-assets-python?branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=3402&branchName=main)

Developed against Python 3.9.1.

## Requirements

- Python 3.7+
- Register a [Client-Credentials Client](https://datahub.connect.aveva.com/clients) in your AVEVA Data Hub tenant and create a client secret to use in the configuration of this sample. ([Video Walkthrough](https://www.youtube.com/watch?v=JPWy0ZX9niU))
- Install required modules: `pip install -r requirements.txt`

## About this sample

This sample uses REST API calls to work with assets and asset types in ADH. It follows a set of steps to demonstrate the usage of various asset endpoints. The assets API reference documentation can be found [here](https://ocs-docs.osisoft.com/Content_Portal/Documentation/Assets/assets.html).

1. Obtain an OAuth token for ADH, using a client-credentials client
1. Create an SDS type
1. Create an SDS stream
1. Insert data into the stream
1. Create an ADH asset
1. Create an ADH asset type
1. Create an asset from an asset type
1. Retrieve an asset
1. Retrieve a resolved asset
1. Update an asset
1. Retrieve the updated asset
1. Retrieve data from an asset
1. Retrieve status for an asset
1. Search for an asset by asset type id
1. Clean up assets, asset types, stream, and type

## Configuring the sample

The sample is configured using the file [appsettings.placeholder.json](appsettings.placeholder.json). Before editing, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

AVEVA Data Hub is secured by obtaining tokens from its identity endpoint. Client credentials clients provide a client application identifier and an associated secret (or key) that are authenticated against the token endpoint. You must replace the placeholders in your `appsettings.json` file with the authentication-related values from your tenant and a client-credentials client created in your ADH tenant.

```json
{
  "Resource": "https://uswe.datahub.connect.aveva.com",
  "ApiVersion": "v1",
  "TenantId": "PLACEHOLDER_REPLACE_WITH_TENANT_ID",
  "NamespaceId": "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID",
  "ClientId": "PLACEHOLDER_REPLACE_WITH_APPLICATION_IDENTIFIER",
  "ClientSecret": "PLACEHOLDER_REPLACE_WITH_APPLICATION_SECRET"
}
```

## Running the sample

To run this example from the command line once the `appsettings.json` is configured, run

```shell
python program.py
```

## Running the automated test

To test the sample, run

```shell
pip install pytest
python -m pytest test.py
```

---

Tested against Python 3.9.1  
For the ADH Assets samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/ASSETS.md)  
For the main ADH samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main AVEVA samples page [ReadMe](https://github.com/osisoft/OSI-Samples)
