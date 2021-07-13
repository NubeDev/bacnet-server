import shortuuid
from abc import abstractmethod

from flask_restful import marshal_with, reqparse
from flask_restful.reqparse import request
from rubix_http.exceptions.exception import NotFoundException
from rubix_http.resource import RubixResource

from src.bacnet_server.models.model_mapping import BPGPointMapping
from src.bacnet_server.models.model_point_store import BACnetPointStoreModel
from src.bacnet_server.resources.model_fields import mapping_bp_gp_fields, paginated_mapping_bp_gp_fields


def sync_point_value(mapping: BPGPointMapping):
    point_store: BACnetPointStoreModel = BACnetPointStoreModel.find_by_point_uuid(mapping.bacnet_point_uuid)
    point_store.sync_point_value_bp_to_gp(mapping.generic_point_uuid)
    return mapping


class BPGPMappingResourceList(RubixResource):
    @classmethod
    @marshal_with(paginated_mapping_bp_gp_fields)
    def get(cls):
        page = request.args.get('page', default=None, type=int)
        per_page = request.args.get('per_page', default=None, type=int)
        sort = request.args.get('sort', default=None, type=str)
        sort_by = request.args.get('sort_by', default=None, type=str)
        search = request.args.get('search', default=None, type=str)
        return BPGPointMapping.find_by_pagination(page, per_page, sort, sort_by, search)

    @classmethod
    @marshal_with(mapping_bp_gp_fields)
    def post(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('bacnet_point_uuid', type=str, required=True)
        parser.add_argument('generic_point_uuid', type=str, required=True)
        parser.add_argument('bacnet_point_name', type=str, required=True)
        parser.add_argument('generic_point_name', type=str, required=True)

        data = parser.parse_args()
        data.uuid = str(shortuuid.uuid())
        mapping: BPGPointMapping = BPGPointMapping(**data)
        mapping.save_to_db()
        sync_point_value(mapping)
        return mapping


class BPGPMappingResourceBase(RubixResource):
    @classmethod
    @marshal_with(mapping_bp_gp_fields)
    def get(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if not mapping:
            raise NotFoundException('Does not exist {uuid}')
        return mapping

    @classmethod
    def delete(cls, uuid):
        mapping = cls.get_mapping(uuid)
        if not mapping:
            raise NotFoundException(f'Does not exist {uuid}')
        mapping.delete_from_db()
        return '', 204

    @classmethod
    @abstractmethod
    def get_mapping(cls, uuid) -> BPGPointMapping:
        raise NotImplementedError


class BPGPMappingResourceByUUID(BPGPMappingResourceBase):
    parser = reqparse.RequestParser()
    parser.add_argument('bacnet_point_uuid', type=str, )
    parser.add_argument('generic_point_uuid', type=str)
    parser.add_argument('bacnet_point_name', type=str)
    parser.add_argument('generic_point_name', type=str)

    @classmethod
    @marshal_with(mapping_bp_gp_fields)
    def patch(cls, uuid):
        data = BPGPMappingResourceByUUID.parser.parse_args()
        mapping = cls.get_mapping(uuid)
        if not mapping:
            raise NotFoundException(f'Does not exist {uuid}')
        BPGPointMapping.filter_by_uuid(uuid).update(data)
        BPGPointMapping.commit()
        output_mapping: BPGPointMapping = cls.get_mapping(uuid)
        sync_point_value(output_mapping)
        return output_mapping

    @classmethod
    def get_mapping(cls, uuid) -> BPGPointMapping:
        return BPGPointMapping.find_by_uuid(uuid)


class GBPMappingResourceByGenericPointUUID(BPGPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> BPGPointMapping:
        return BPGPointMapping.find_by_generic_point_uuid(uuid)


class GBPMappingResourceByBACnetPointUUID(BPGPMappingResourceBase):
    @classmethod
    def get_mapping(cls, uuid) -> BPGPointMapping:
        return BPGPointMapping.find_by_bacnet_point_uuid(uuid)
