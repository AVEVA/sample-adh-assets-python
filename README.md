# OSIsoft Cloud Services Assets Python Sample

**Version:** 1.0.2

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OCS/osisoft.sample-ocs-assets-python?branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=3402&branchName=main)

Developed against Python 3.9.1.

## Requirements

- Python 3.9+
- Register a [Client-Credentials Client](https://cloud.osisoft.com/clients) in your OSIsoft Cloud Services tenant and create a client secret to use in the configuration of this sample. ([Video Walkthrough](https://www.youtube.com/watch?v=JPWy0ZX9niU))
- Install required modules: `pip install -r requirements.txt`

## About this sample

This sample uses REST API calls to work with assets and asset types in OCS. It follows a set of steps to demonstrate the usage of various asset endpoints. The assets API reference documentation can be found [here](https://ocs-docs.osisoft.com/Content_Portal/Documentation/Assets/assets.html).

1. Obtain an OAuth token for OCS, using a client-credentials client
1. Create an SDS type
1. Create an SDS stream
1. Insert data into the stream
1. Create an OCS asset
1. Create an OCS asset type
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

The sample is configured using the file [config.placeholder.ini](config.placeholder.ini). Before editing, rename this file to `config.ini`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

OSIsoft Cloud Services is secured by obtaining tokens from its identity endpoint. Client credentials clients provide a client application identifier and an associated secret (or key) that are authenticated against the token endpoint. You must replace the placeholders in your `config.ini` file with the authentication-related values from your tenant and a client-credentials client created in your OCS tenant.

```ini
[Configuration]
Resource = https://dat-b.osisoft.com
ApiVersion = v1-preview
TenantId = REPLACE_WITH_TENANT_ID
NamespaceId = REPLACE_WITH_NAMESPACE_ID
ClientId = REPLACE_WITH_APPLICATION_IDENTIFIER
ClientSecret = REPLACE_WITH_APPLICATION_SECRET
```

## Running the sample

To run this example from the command line once the `config.ini` is configured, run

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

For the main OCS samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main OSIsoft samples page [ReadMe](https://github.com/osisoft/OSI-Samples)
