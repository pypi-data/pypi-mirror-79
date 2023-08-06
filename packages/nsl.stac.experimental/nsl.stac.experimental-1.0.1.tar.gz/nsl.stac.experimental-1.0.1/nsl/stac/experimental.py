import boto3
import botocore.exceptions

from datetime import date, timezone
from datetime import datetime as internal_datetime
from typing import Union, Iterator

from google.protobuf.any_pb2 import Any
from google.protobuf.wrappers_pb2 import FloatValue
from epl.geometry import Polygon

from nsl.stac import StacItem, StacRequest, View, ViewRequest,\
    Mosaic, MosaicRequest, Eo, EoRequest, EnvelopeData, FloatFilter, Asset, enum, utils
from nsl.stac.client import NSLClient
from nsl.stac import stac_service as stac_singleton





def set_properties(stac_data, properties, type_url_prefix):
    """
     pack properties and then set the properties member value to the input.
     :param stac_data:
     :param properties:
     :return:
     """
    if properties is None:
        return

    # pack the properties into an Any field
    packed_properties = Any()
    packed_properties.Pack(properties,
                           type_url_prefix=type_url_prefix + properties.DESCRIPTOR.full_name)

    # overwrite the previous properties field with this updated version
    stac_data.properties.CopyFrom(packed_properties)
    properties = properties
    return stac_data, properties


def _check_assets_exist(stac_item: StacItem, b_raise=True):
    results = []
    for asset_key in stac_item.assets:
        asset = stac_item.assets[asset_key]
        b_file_exists = _check_asset_exists(asset)

        if not b_file_exists and b_raise:
            raise ValueError("get_blob_metadata returns false for asset key {}".format(asset_key))
        results.append(asset_key)
    return results


def _check_asset_exists(asset: Asset) -> bool:
    if asset.cloud_platform == enum.CloudPlatform.GCP:
        return utils.get_blob_metadata(bucket=asset.bucket, blob_name=asset.object_path) is not None
    elif asset.cloud_platform == enum.CloudPlatform.AWS:
        return _check_aws_asset_exists(asset)
    else:
        raise ValueError("cloud platform {0} of asset {1} not supported"
                         .format(enum.CloudPlatform(asset.cloud_platform).name, asset))


def _check_aws_asset_exists(asset: Asset) -> bool:
    s3 = boto3.client('s3')

    try:
        s3.head_object(Bucket=asset.bucket, Key=asset.object_path, RequestPayer='requester')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise e
    return True

class _BaseWrap:
    def __init__(self, stac_data, properties_func, type_url_prefix="nearspacelabs.com/proto/"):
        """
        Whether it's a stac_request or a stac_item, allow for the repack_properties method to work
        :param stac_data:
        :param properties_func:
        """
        self._stac_data = stac_data
        self.properties = None
        self._properties_func = properties_func

        if stac_data is not None and stac_data.HasField("properties"):
            self.properties = properties_func()
            self._stac_data.properties.Unpack(self.properties)
        elif properties_func is not None:
            self.properties = properties_func()
            self._set_properties(self.properties, type_url_prefix)

    def __str__(self):
        return str(self._stac_data)

    def _set_properties(self, properties, type_url_prefix):
        self._stac_data, self.properties = set_properties(self._stac_data, properties, type_url_prefix)

    def get_field(self, metadata_key: str, key: str):
        if self.properties.HasField(metadata_key):
            return getattr(getattr(self.properties, metadata_key), key)
        return None

    def get_wrapped_field(self, metadata_key: str, key: str):
        if self.properties.HasField(metadata_key):
            return getattr(getattr(getattr(self.properties, metadata_key), key), "value")
        return None

    def set_internal_sub_object(self, metadata_key: str):
        pass

    def set_field(self, metadata_key: str, key: str, value):
        self.set_internal_sub_object(metadata_key)
        setattr(getattr(self.properties, metadata_key), key, value)

    def set_obj(self, metadata_key: str, key: str, value):
        self.set_internal_sub_object(metadata_key)
        getattr(getattr(self.properties, metadata_key), key).CopyFrom(value)

    def set_nested_obj(self, metadata_key: str, object_key: str, value_key: str, value):
        self.set_internal_sub_object(metadata_key)
        getattr(getattr(getattr(self.properties, metadata_key), object_key), value_key).CopyFrom(value)

    def set_nested_field(self, metadata_key: str, object_key: str, value_key: str, value):
        setattr(getattr(getattr(self.properties, metadata_key), object_key), value_key, value)

    def get_nested_field(self, metadata_key: str, object_key: str, value_key: str):
        if self.properties.HasField(metadata_key):
            return getattr(getattr(getattr(self.properties, metadata_key), object_key), value_key)
        return None

    def get_nested_wrapped_field(self, metadata_key: str, object_key: str, value_key: str):
        if self.properties.HasField(metadata_key):
            return getattr(getattr(getattr(getattr(self.properties, metadata_key), object_key), value_key), "value")
        return None


class StacItemWrap(_BaseWrap):
    def __init__(self, stac_item: StacItem = None, properties_constructor=None):
        if stac_item is None:
            stac_data = StacItem()
        else:
            stac_data = StacItem()
            stac_data.CopyFrom(stac_item)
        super().__init__(stac_data, properties_constructor)
        self.local_asset_data = {}

    @property
    def cloud_cover(self):
        """
        get cloud cover value
        :return: float or None
        """
        if self.stac_item.HasField("eo") and self.stac_item.eo.HasField("cloud_cover"):
            return self.stac_item.eo.cloud_cover.value
        return None

    @cloud_cover.setter
    def cloud_cover(self, value: float):
        if not self.stac_item.HasField("eo"):
            self.stac_item.eo.CopyFrom(Eo(cloud_cover=FloatValue(value=value)))
        else:
            self.stac_item.eo.cloud_cover.CopyFrom(FloatValue(value=value))

    @property
    def collection(self):
        return self.stac_item.collection

    @collection.setter
    def collection(self, value: str):
        self.stac_item.collection = value

    @property
    def constellation(self):
        return self.stac_item.constellation_enum

    @constellation.setter
    def constellation(self, value: enum.Constellation):
        self.stac_item.constellation_enum = value

    # TODO something about this datetime is preventing us from importing datetime
    @property
    def datetime(self):
        return self.observed

    @datetime.setter
    def datetime(self, value: Union[internal_datetime, date]):
        self.observed = value

    @property
    def end_datetime(self):
        return self.stac_item.end_observed

    @end_datetime.setter
    def end_datetime(self, value: Union[internal_datetime, date]):
        self.end_observed = value

    @property
    def end_observed(self):
        return self.stac_item.end_observed

    @end_observed.setter
    def end_observed(self, value: Union[internal_datetime, date]):
        self.stac_item.end_observed.CopyFrom(utils.pb_timestamp(d_utc=value))
        self.stac_item.end_observed.CopyFrom(utils.pb_timestamp(d_utc=value))

    @property
    def geometry(self) -> Polygon:
        if self.stac_item.HasField("geometry"):
            return Polygon.import_protobuf(self.stac_item.geometry)
        elif self.stac_item.HasField("bbox"):
            return Polygon.from_envelope_data(self.stac_item.bbox)

    @geometry.setter
    def geometry(self, polygon: Polygon):
        self.stac_item.geometry.CopyFrom(polygon.geometry_data)
        self.stac_item.bbox.CopyFrom(polygon.envelope_data)

    @property
    def gsd(self):
        """
        get cloud cover value
        :return: float or None
        """
        if self.stac_item.HasField("gsd"):
            return self.stac_item.gsd.value
        return None

    @gsd.setter
    def gsd(self, value: float):
        self.stac_item.gsd.CopyFrom(FloatValue(value=value))

    @property
    def id(self):
        return self.stac_item.id

    @id.setter
    def id(self, value: str):
        self.stac_item.id = value

    @property
    def instrument(self):
        return self.stac_item.instrument_enum

    @instrument.setter
    def instrument(self, value: enum.Instrument):
        self.stac_item.instrument_enum = value

    @property
    def mission(self):
        return self.stac_item.mission_enum

    @mission.setter
    def mission(self, value: enum.Mission):
        self.stac_item.mission_enum = value

    @property
    def mosaic_name(self):
        if self.stac_item.HasField("mosaic"):
            return self.stac_item.mosaic.name
        return None

    @mosaic_name.setter
    def mosaic_name(self, name: str):
        if not self.stac_item.HasField("mosaic"):
            self.stac_item.mosaic.CopyFrom(Mosaic(name=name))
        else:
            self.stac_item.mosaic.name = name

    @property
    def mosaic_quad_key(self) -> str:
        """
If the STAC item is a quad from a mosaic, then it has a quad key that defines the boundaries of the quad. The quad tree
definition is assumed to be the convention defined by Google Maps, based off of there Pseudo-Web Mercator projection.

An example quad key is '02313012030231'. Quads use 2-bit tile interleaved addresses. The first character defines the
largest quadrant (in this case 0 is upper left), the next character ('2') is the upper right quadrant of that first
quadrant, the 3rd character ('3') is the lower left quadrant of the previous quadrant and so on.

For more details on the quad tree tiling for maps use `openstreetmaps docs
<https://wiki.openstreetmap.org/wiki/QuadTiles#Quadtile_implementation>`
        :return:
        """
        if self.stac_item.HasField("mosaic"):
            return self.stac_item.mosaic.quad_key
        return None

    @mosaic_quad_key.setter
    def mosaic_quad_key(self, quad_key: str):
        if not self.stac_item.HasField("mosaic"):
            self.stac_item.mosaic.CopyFrom(Mosaic(quad_key=quad_key))
        else:
            self.stac_item.mosaic.quad_key = quad_key

    @property
    def observed(self) -> internal_datetime:
        if self.stac_item.HasField("datetime"):
            return internal_datetime.fromtimestamp(self.stac_item.datetime.seconds, tz=timezone.utc)
        elif self.stac_item.HasField("observed"):
            return internal_datetime.fromtimestamp(self.stac_item.observed.seconds, tz=timezone.utc)
        else:
            return None

    @observed.setter
    def observed(self, value: Union[internal_datetime, date]):
        self.stac_item.datetime.CopyFrom(utils.pb_timestamp(d_utc=value))
        self.stac_item.observed.CopyFrom(utils.pb_timestamp(d_utc=value))

    @property
    def off_nadir(self) -> float:
        """
        get cloud cover value
        :return: float or None
        """
        if self.stac_item.HasField("view") and self.stac_item.view.HasField("off_nadir"):
            return self.stac_item.view.off_nadir.value
        return None

    @off_nadir.setter
    def off_nadir(self, value: float):
        if not self.stac_item.HasField("view"):
            self.stac_item.view.CopyFrom(View(off_nadir=FloatValue(value=value)))
        else:
            self.stac_item.view.off_nadir.CopyFrom(FloatValue(value=value))

    @property
    def platform(self):
        return self.stac_item.platform_enum

    @platform.setter
    def platform(self, value: enum.Platform):
        self.stac_item.platform_enum = value

    @property
    def created(self) -> internal_datetime:
        if self.stac_item.HasField("created"):
            return internal_datetime.fromtimestamp(self.stac_item.created.seconds, tz=timezone.utc)
        else:
            return None

    @created.setter
    def created(self, value: Union[internal_datetime, date]):
        self.stac_item.created.CopyFrom(utils.pb_timestamp(d_utc=value))

    @property
    def provenance_ids(self):
        """
The stac_ids that went into creating the current mosaic. They are in the array in the order which they were used in
the mosaic
        :return:
        """
        return self.stac_item.mosaic.provenance_ids

    @property
    def stac_item(self):
        """
        get stac_item
        :return: StacItem
        """
        return self._stac_data

    @property
    def updated(self) -> internal_datetime:
        if self.stac_item.HasField("updated"):
            return internal_datetime.fromtimestamp(self.stac_item.updated.seconds, tz=timezone.utc)
        else:
            return None

    @updated.setter
    def updated(self, value: Union[internal_datetime, date]):
        self.stac_item.updated.CopyFrom(utils.pb_timestamp(d_utc=value))

    def check_assets_exist(self, b_raise):
        return _check_assets_exist(self.stac_item, b_raise=b_raise)


class StacRequestWrap(_BaseWrap):
    def __init__(self, stac_request: StacRequest = None, properties_constructor=None, id: str = ""):
        if stac_request is None:
            stac_request = StacRequest(id=id)

        super().__init__(stac_request, properties_constructor)

    @property
    def bbox(self) -> EnvelopeData:
        if self.stac_request.HasField("bbox"):
            return self.stac_request.bbox
        return None

    @bbox.setter
    def bbox(self, value: EnvelopeData):
        self.stac_request.bbox.CopyFrom(value)
        self.stac_request.ClearField("intersects")

    @property
    def collection(self) -> str:
        return self.stac_request.collection

    @collection.setter
    def collection(self, value: str):
        self.stac_request.collection = value

    @property
    def constellation(self):
        return self.stac_request.constellation_enum

    @constellation.setter
    def constellation(self, value: enum.Constellation):
        self.stac_request.constellation_enum = value

    @property
    def intersects(self):
        if self.stac_request.HasField("intersects"):
            return Polygon.import_protobuf(self.stac_request.intersects)
        return None

    @intersects.setter
    def intersects(self, polygon: Polygon):
        self.stac_request.intersects.CopyFrom(polygon.geometry_data)
        self.stac_request.ClearField("bbox")

    @property
    def id(self):
        return self.stac_request.id

    @id.setter
    def id(self, value):
        self.stac_request.id = value

    @property
    def instrument(self):
        return self.stac_request.instrument_enum

    @instrument.setter
    def instrument(self, value: enum.Instrument):
        self.stac_request.instrument_enum = value

    @property
    def limit(self):
        return self.stac_request.limit

    @limit.setter
    def limit(self, value: int):
        self.stac_request.limit = value

    @property
    def mission(self):
        return self.stac_request.mission_enum

    @mission.setter
    def mission(self, value: enum.Mission):
        self.stac_request.mission_enum = value

    @property
    def mosaic_name(self):
        if self.stac_request.HasField("mosaic"):
            return self.stac_request.mosaic.name
        return None

    @mosaic_name.setter
    def mosaic_name(self, value):
        if not self.stac_request.HasField("mosaic"):
            self.stac_request.mosaic.CopyFrom(MosaicRequest(name=value))
        else:
            self.stac_request.mosaic.name = value

    @property
    def offset(self):
        return self.stac_request.offset

    @offset.setter
    def offset(self, value: int):
        self.stac_request.offset = value

    @property
    def platform(self):
        return self.stac_request.platform_enum

    @platform.setter
    def platform(self, value: enum.Platform):
        self.stac_request.platform_enum = value

    @property
    def mosaic_quad_key(self):
        """
Overview of :func:`~StacItemWrap.mosaic_quad_key`

The quad_key to search for mosaic quad STAC items by. If a quad STAC item exists with the key '02313012030231' and this
'mosaic_quad_key' is set to the key of a smaller internal quad, like '02313012030231300', '02313012030231301',
'023130120302313', etc, then the aforementioned '02313012030231' STAC item will be returned.

If a 'mosaic_quad_key' is set to a larger quad, like '02313012030', then the '02313012030231' quad STAC item and many
other quad STAC items that are contained by '02313012030' are returned.
        :return:
        """
        if self.stac_request.HasField("mosaic"):
            return self.stac_request.mosaic.quad_key
        return None

    @mosaic_quad_key.setter
    def mosaic_quad_key(self, value):
        if not self.stac_request.HasField("mosaic"):
            self.stac_request.mosaic.CopyFrom(MosaicRequest(quad_key=value))
        else:
            self.stac_request.mosaic.quad_key = value

    @property
    def stac_request(self):
        return self._stac_data

    def set_full_limit(self):
        self.limit = self._client.count_ex(stac_request_wrapped=self)

    def set_off_nadir(self, value: float,
                      rel_type: enum.FilterRelationship,
                      sort_direction: enum.SortDirection = enum.SortDirection.NOT_SORTED):
        off_nadir_value = FloatFilter(value=value, rel_type=rel_type, sort_direction=sort_direction)
        if not self.stac_request.HasField("view"):
            self.stac_request.view.CopyFrom(ViewRequest(off_nadir=off_nadir_value))
        else:
            self.stac_request.view.off_nadir.CopyFrom(off_nadir_value)

    def set_cloud_cover(self,
                        rel_type: enum.FilterRelationship,
                        value: float = None,
                        start: float = None,
                        end: float = None,
                        sort_direction: enum.SortDirection = enum.SortDirection.NOT_SORTED):
        if not self.stac_request.HasField("eo"):
            self.stac_request.eo.CopyFrom(EoRequest())
            self.set_cloud_cover(rel_type=rel_type, value=value, start=start, end=end, sort_direction=sort_direction)
        float_filter = FloatFilter(rel_type=rel_type,
                                   value=value,
                                   start=start,
                                   end=end,
                                   sort_direction=sort_direction)
        self.stac_request.eo.cloud_cover.CopyFrom(float_filter)

    def set_gsd(self,
                value: float,
                rel_type: enum.FilterRelationship,
                sort_direction: enum.SortDirection = enum.SortDirection.NOT_SORTED):
        gsd_value = FloatFilter(value=value, rel_type=rel_type, sort_direction=sort_direction)
        self.stac_request.gsd.CopyFrom(gsd_value)

    def set_observed(self,
                     rel_type: enum.FilterRelationship,
                     value: Union[internal_datetime, date] = None,
                     start: Union[internal_datetime, date] = None,
                     end: Union[internal_datetime, date] = None,
                     sort_direction: enum.SortDirection = enum.SortDirection.NOT_SORTED,
                     tzinfo: timezone = timezone.utc):
        self._stac_data.observed.CopyFrom(utils.pb_timestampfield(rel_type=rel_type,
                                                                  value=value,
                                                                  start=start,
                                                                  end=end,
                                                                  sort_direction=sort_direction,
                                                                  tzinfo=tzinfo))

    def set_created(self,
                    rel_type: enum.FilterRelationship,
                    value: Union[internal_datetime, date] = None,
                    start: Union[internal_datetime, date] = None,
                    end: Union[internal_datetime, date] = None,
                    sort_direction: enum.SortDirection = enum.SortDirection.NOT_SORTED,
                    tzinfo: timezone = timezone.utc):
        self._stac_data.created.CopyFrom(utils.pb_timestampfield(rel_type=rel_type,
                                                                 value=value,
                                                                 start=start,
                                                                 end=end,
                                                                 sort_direction=sort_direction,
                                                                 tzinfo=tzinfo))

    def set_updated(self,
                    rel_type: enum.FilterRelationship,
                    value: Union[internal_datetime, date] = None,
                    start: Union[internal_datetime, date] = None,
                    end: Union[internal_datetime, date] = None,
                    sort_direction: enum.SortDirection = enum.SortDirection.NOT_SORTED,
                    tzinfo: timezone = timezone.utc):
        self._stac_data.updated.CopyFrom(utils.pb_timestampfield(rel_type=rel_type,
                                                                 value=value,
                                                                 start=start,
                                                                 end=end,
                                                                 sort_direction=sort_direction,
                                                                 tzinfo=tzinfo))


class NSLClientEx(NSLClient):
    def __init__(self, nsl_only=False):
        super().__init__(nsl_only=nsl_only)
        self._internal_stac_service = stac_singleton

    def update_service_url(self, stac_service_url):
        """
        update the stac service address
        :param stac_service_url: localhost:8080, 34.34.34.34:9000, http://demo.nearspacelabs.com, etc
        :return:
        """
        super().update_service_url(stac_service_url)
        self._internal_stac_service.update_service_url(stac_service_url=stac_service_url)

    def search_ex(self, stac_request_wrapped: StacRequestWrap, timeout=15) -> Iterator[StacItemWrap]:
        for stac_item in self.search(stac_request_wrapped.stac_request, timeout=timeout):
            yield StacItemWrap(stac_item=stac_item)

    def search_one_ex(self, stac_request_wrapped: StacRequestWrap, timeout=15) -> StacItemWrap:
        return StacItemWrap(self.search_one(stac_request=stac_request_wrapped.stac_request, timeout=timeout))

    def count_ex(self, stac_request_wrapped: StacRequestWrap, timeout=15) -> int:
        return self.count(stac_request=stac_request_wrapped.stac_request, timeout=timeout)
