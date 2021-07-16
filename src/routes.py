from flask import Blueprint
from flask_restful import Api

from src.bacnet_server.resources.mapping.mapping import BPGPMappingResourceList, GBPMappingResourceByGenericPointUUID, \
    GBPMappingResourceByBACnetPointUUID, BPGPMappingResourceByUUID, BPGPMappingResourceListByUUID, \
    BPGPMappingResourceListByName, BPGPMappingResourceUpdateMappingState
from src.bacnet_server.resources.point.point_plural import BACnetPointPlural
from src.bacnet_server.resources.point.point_singular import BACnetPointSingularByUUID, \
    BACnetPointSingularByName, BACnetPointSingularByObject
from src.bacnet_server.resources.point.point_sync import BPToGPSync, MPSync
from src.bacnet_server.resources.server.server import BACnetServer
from src.system.resources.ping import Ping

bp_bacnet_server = Blueprint('bacnet_server', __name__, url_prefix='/api/bacnet')
api_bacnet_server = Api(bp_bacnet_server)

api_bacnet_server.add_resource(BACnetServer, '/server')
api_bacnet_server.add_resource(BACnetPointPlural, '/points')
api_bacnet_server.add_resource(BACnetPointSingularByUUID, '/points/uuid/<string:uuid>')
api_bacnet_server.add_resource(BACnetPointSingularByObject, '/points/obj/<string:object_type>/<string:address>')
api_bacnet_server.add_resource(BACnetPointSingularByName, '/points/name/<string:object_name>')

# BACnet points <> Generic points mappings
bp_mapping_bp_gp = Blueprint('mappings_bp_gp', __name__, url_prefix='/api/mappings/bp_gp')
api_mapping_bp_gp = Api(bp_mapping_bp_gp)
api_mapping_bp_gp.add_resource(BPGPMappingResourceList, '')
api_mapping_bp_gp.add_resource(BPGPMappingResourceListByUUID, '/uuid')
api_mapping_bp_gp.add_resource(BPGPMappingResourceListByName, '/name')
api_mapping_bp_gp.add_resource(BPGPMappingResourceByUUID, '/uuid/<string:uuid>')
api_mapping_bp_gp.add_resource(GBPMappingResourceByBACnetPointUUID, '/bacnet/<string:uuid>')
api_mapping_bp_gp.add_resource(GBPMappingResourceByGenericPointUUID, '/generic/<string:uuid>')
api_mapping_bp_gp.add_resource(BPGPMappingResourceUpdateMappingState, '/update_mapping_state')

bp_sync = Blueprint('sync_bp_gp', __name__, url_prefix='/api/sync')
api_sync = Api(bp_sync)
api_sync.add_resource(BPToGPSync, '/bp_to_gp')
api_sync.add_resource(MPSync, '/mp')

bp_system = Blueprint('system', __name__, url_prefix='/api/system')
api_system = Api(bp_system)
api_system.add_resource(Ping, '/ping')
