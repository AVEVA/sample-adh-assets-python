import json
import math
import time
import traceback

from ocs_sample_library_preview import (Asset, AssetType, MetadataItem, ADHClient, SdsType,
                                        SdsTypeCode, SdsTypeProperty, SdsStream, StatusEnum,
                                        StatusMapping, StreamReference, TypeReference,
                                        ValueStatusMapping, StatusConfiguration,
                                        StatusDefinitionType)

from wave_data import WaveData

def get_appsettings():
    """Open and parse the appsettings.json file"""

    # Try to open the configuration file
    try:
        with open(
            'appsettings.json',
            'r',
        ) as f:
            appsettings = json.load(f)
    except Exception as error:
        print(f'Error: {str(error)}')
        print(f'Could not open/read appsettings.json')
        exit()

    return appsettings


def get_wave_data_type(sample_type_id):
    """Creates an SDS type definition for WaveData"""

    if sample_type_id is None or not isinstance(sample_type_id, str):
        raise TypeError('sample_type_id is not an instantiated string')

    int_type = SdsType('intType', SdsTypeCode.Int32)
    double_type = SdsType('doubleType', SdsTypeCode.Double)

    # WaveData uses Order as the key, or primary index
    order_property = SdsTypeProperty('Order', True, int_type)
    tau_property = SdsTypeProperty('Tau', False, double_type)
    radians_property = SdsTypeProperty('Radians', False, double_type)
    sin_property = SdsTypeProperty('Sin', False, double_type)
    cos_property = SdsTypeProperty('Cos', False, double_type)
    tan_property = SdsTypeProperty('Tan', False, double_type)
    sinh_property = SdsTypeProperty('Sinh', False, double_type)
    cosh_property = SdsTypeProperty('Cosh', False, double_type)
    tanh_property = SdsTypeProperty('Tanh', False, double_type)

    # Create an SdsType for WaveData Class
    wave = SdsType(sample_type_id, SdsTypeCode.Object,
                   [order_property, tau_property, radians_property, sin_property, cos_property,
                    tan_property, sinh_property, cosh_property, tanh_property], 'WaveDataSample',
                   'This is a sample SDS type for storing WaveData type events')

    return wave


def next_wave(order: float, multiplier: float):
    radians = (order) * math.pi/32

    wave_data = WaveData(order,
                         radians / (2 * math.pi), radians,
                         multiplier * math.sin(radians),
                         multiplier * math.cos(radians),
                         multiplier * math.tan(radians),
                         multiplier * math.sinh(radians),
                         multiplier * math.cosh(radians),
                         multiplier * math.tanh(radians))

    return wave_data


def suppress_error(sds_call):
    try:
        sds_call()
    except Exception as error:
        print(f"Suppressed error: {error}")


def main(test=False):
    exception: Exception = None

    # IDs
    type_id = 'WaveDataTypeId'
    stream_id = 'WaveStreamId'
    simple_asset_id = 'SimpleAssetId'
    stream_reference_id = 'StreamReferenceId'
    type_metadata_id = 'TypeMetadataId'
    asset_type_id = 'AssetTypeId'
    asset_metadata_id = 'AssetMetadataId'
    asset_id = 'AssetId'

    # Names
    stream_name = 'WaveStream'
    simple_asset_name = 'SimpleAsset'
    stream_reference_name = 'StreamReference'
    type_metadata_name = 'TypeMetadata'
    asset_type_name = 'AssetType'
    asset_metadata_name = 'AssetMetadata'
    asset_name = 'AssetName'

    # UOM
    type_metadata_uom = 'V'
    asset_metadata_uom = 'mV'

    try:
        appsettings = get_appsettings()

        resource = appsettings.get('Resource')
        api_version = appsettings.get('ApiVersion')
        tenant_id = appsettings.get('TenantId')
        namespace_id = appsettings.get('NamespaceId')
        client_id = appsettings.get('ClientId')
        client_secret = appsettings.get('ClientSecret')

        print(r'-----------------------------------')
        print(r'   ___                   _         ')
        print(r'  / _ \                 | |        ')
        print(r' / /_\ \ ___  ___   ___ | |_  ___  ')
        print(r' |  _  |/ __|/ __| / _ \| __|/ __| ')
        print(r' | | | |\__ \\__ \| __/| | _ \__ \ ')
        print(r' \_| |_/|___/|___/ \___| \__||___/ ')
        print(r'-----------------------------------')
        print()
        print(f'SDS endpoint at {resource}')

        # Step 1: Obtain an OAuth token for ADH, using a client-credentials client
        print()
        print('Step 1: Setting up ADHClient for authentication and requests...')
        adh_client = ADHClient(api_version, tenant_id,
                               resource, client_id, client_secret)

        # Step 2: Create an SDS type
        print()
        print('Step 2: Creating an SdsType...')
        wave_type = get_wave_data_type(type_id)
        wave_type = adh_client.Types.getOrCreateType(namespace_id, wave_type)

        # Step 3: Create an SDS stream
        print()
        print('Step 3: Creating an SdsStream...')
        wave_stream = SdsStream(stream_id, wave_type.Id, stream_name)
        wave_stream = adh_client.Streams.getOrCreateStream(
            namespace_id, wave_stream)

        # Step 4: Insert data into the stream
        print()
        print('Step 4: Inserting data...')
        waves = []
        for event in range(0, 20, 2):
            waves.append(next_wave(event, 2.0).toDictionary())
        adh_client.Streams.updateValues(
            namespace_id, wave_stream.Id, json.dumps(waves))

        # Step 5: Create an ADH asset
        print()
        print('Step 5: Creating simple Asset...')
        simple_asset = Asset(
            simple_asset_id, simple_asset_name, 'My First Asset!')
        adh_client.Assets.createOrUpdateAsset(namespace_id, simple_asset)

        # Step 6: Create an ADH asset type
        print()
        print('Step 6: Creating AssetType...')
        type_metadata = MetadataItem(type_metadata_id, type_metadata_name,
                                     'We are going to use this metadata to show inheritance',
                                     SdsTypeCode.Int64, type_metadata_uom)
        type_reference = TypeReference(
            stream_reference_id, stream_reference_name, wave_type.Id)
        status_configuration = StatusConfiguration(
            StatusDefinitionType.StreamPropertyMapping,
            StatusMapping(type_reference.StreamReferenceId, 'Order', [
                ValueStatusMapping(0, StatusEnum.Warning),
                ValueStatusMapping(10, StatusEnum.Good),
                ValueStatusMapping(18, StatusEnum.Bad)
            ]))
        asset_type = AssetType(asset_type_id, asset_type_name, 'My first AssetType!', [
                               type_metadata], [type_reference], status_configuration)
        asset_type = adh_client.AssetTypes.createOrUpdateAssetType(
            namespace_id, asset_type)

        # Step 7: Create an asset from an asset type
        print()
        print('Step 7: Creating Asset with AssetType...')
        stream_reference = StreamReference(
            stream_reference_id, stream_id=wave_stream.Id)
        inherited_metadata = MetadataItem(type_metadata_id)
        asset_metadata = MetadataItem(asset_metadata_id, asset_metadata_name,
                                      'Simple Metadata set on Asset', SdsTypeCode.Double,
                                      asset_metadata_uom)
        asset = Asset(asset_id, asset_name, asset_type_id=asset_type.Id, metadata=[
                      inherited_metadata, asset_metadata], stream_references=[stream_reference])
        asset = adh_client.Assets.createOrUpdateAsset(namespace_id, asset)

        # Step 8: Retrieve an asset
        print()
        print('Step 8: Getting an Asset...')
        asset = adh_client.Assets.getAssetById(namespace_id, asset_id)
        print(f'Returned Asset has Id {asset.Id} and Name {asset.Name}')

        # Step 9: Retrieve a resolved asset
        print()
        print('Step 9: Getting a ResolvedAsset...')
        asset = adh_client.Assets.getResolvedAsset(namespace_id, asset_id)
        print('Asset null values are overridden by its AssetType, if any, when resolved. ' +
              f'ResolvedAsset Description: {asset.Description}')

        # Step 10: Update an asset
        print()
        print('Step 10: Updating an Asset Description...')
        asset = Asset(asset_id, asset_name, 'My first Asset with AssetType!', asset_type.Id, [
            inherited_metadata, asset_metadata], [stream_reference])
        asset = adh_client.Assets.createOrUpdateAsset(namespace_id, asset)

        # Step 11: Retrieve the updated asset
        print()
        print('Step 11: Getting the updated Asset...')
        asset = adh_client.Assets.getAssetById(namespace_id, asset_id)
        print(asset.toJson())

        # Step 12: Retrieve data from an asset
        print()
        print('Step 12: Getting last DataResults from an Asset...')
        data = adh_client.Assets.getAssetLastData(namespace_id, asset_id)
        print(data.toJson())

        # Step 13: Retrieve status for an asset
        print()
        print('Step 13: Update last Status from an Asset...')
        time.sleep(5)  # Give ADH a chance to catch up before requesting status
        status = adh_client.Assets.getAssetStatus(namespace_id, asset_id)
        print(status.toJson())

        # Step 14: Search for an asset by asset type id
        print()
        print('Step 14: Searching for an Asset by AssetTypeId...')
        assets = adh_client.Assets.getAssets(
            namespace_id, f'AssetTypeId:{asset_type_id}')
        for value in assets:
            print(value.toJson())

    except Exception as error:
        print()
        print((f'Encountered error: {error}'))
        print()
        traceback.print_exc()
        exception = error

    finally:
        # Step 15: Clean up assets, asset types, stream, and type
        print()
        print('Step 15: Cleaning up...')
        print('Deleting Asset...')
        suppress_error(lambda: adh_client.Assets.deleteAsset(
            namespace_id, asset_id))
        print('Deleting AssetType...')
        suppress_error(lambda: adh_client.AssetTypes.deleteAssetType(
            namespace_id, asset_type_id))
        print('Deleting simple Asset...')
        suppress_error(lambda: adh_client.Assets.deleteAsset(
            namespace_id, simple_asset_id))
        print('Deleting SdsStream...')
        suppress_error(lambda: adh_client.Streams.deleteStream(
            namespace_id, stream_id))
        print('Deleting SdsType...')
        suppress_error(lambda: adh_client.Types.deleteType(
            namespace_id, type_id))

        if test and exception is not None:
            raise exception

    print('Complete!')


if __name__ == '__main__':
    main()
