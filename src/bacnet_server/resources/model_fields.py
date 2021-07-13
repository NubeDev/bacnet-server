from collections import OrderedDict

from flask_restful import fields

paginated_fields = {
    "page": fields.Integer,
    "per_page": fields.Integer,
    "pages": fields.Integer,
    "total": fields.Integer,
    "has_prev": fields.Boolean,
    "prev_num": fields.Integer,
    "has_next": fields.Boolean,
    "next_num": fields.Integer,
}

point_store_fields = {
    'present_value': fields.String,
    'ts': fields.String
}

priority_array_write_fields = OrderedDict({
    '_1': fields.Float,
    '_2': fields.Float,
    '_3': fields.Float,
    '_4': fields.Float,
    '_5': fields.Float,
    '_6': fields.Float,
    '_7': fields.Float,
    '_8': fields.Float,
    '_9': fields.Float,
    '_10': fields.Float,
    '_11': fields.Float,
    '_12': fields.Float,
    '_13': fields.Float,
    '_14': fields.Float,
    '_15': fields.Float,
    '_16': fields.Float,
})

point_fields = {
    'uuid': fields.String,
    'object_type': fields.String(attribute="object_type.name"),
    'object_name': fields.String,
    'use_next_available_address': fields.Boolean,
    'address': fields.Integer,
    'relinquish_default': fields.Float,
    'priority_array_write': fields.Nested(priority_array_write_fields),
    'event_state': fields.String(attribute="event_state.name"),
    'units': fields.String(attribute="units.name"),
    'description': fields.String,
    'enable': fields.Boolean,
    'fault': fields.Boolean,
    'data_round': fields.Integer,
    'data_offset': fields.Float,
    'cov': fields.Float,
    'source': fields.String(attribute="source.name"),
    'created_on': fields.String,
    'updated_on': fields.String,
    'point_store': fields.Nested(point_store_fields)
}

paginated_point_fields = {
    **paginated_fields,
    "items": fields.Nested(point_fields),
}
server_field = {
    'ip': fields.String,
    'port': fields.Integer,
    'device_id': fields.String,
    'local_obj_name': fields.String,
    'model_name': fields.String,
    'vendor_id': fields.String,
    'vendor_name': fields.String,
}

mapping_bp_gp_fields = {
    'uuid': fields.String,
    'bacnet_point_uuid': fields.String,
    'generic_point_uuid': fields.String,
    'bacnet_point_name': fields.String,
    'generic_point_name': fields.String,
}

paginated_mapping_bp_gp_fields = {
    **paginated_fields,
    "items": fields.Nested(mapping_bp_gp_fields),
}
