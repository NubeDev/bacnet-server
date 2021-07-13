from flask import Response
from rubix_http.request import gw_request
from sqlalchemy import desc, asc, or_
from sqlalchemy.orm import validates

from src import db
from src.bacnet_server.models.model_base import ModelBase


class BPGPointMapping(ModelBase):
    __tablename__ = 'mappings_bp_gp'

    uuid = db.Column(db.String, primary_key=True)
    bacnet_point_uuid = db.Column(db.String(80), db.ForeignKey('bac_points.uuid'), nullable=False)
    generic_point_uuid = db.Column(db.String, nullable=False, unique=True)
    bacnet_point_name = db.Column(db.String(80), nullable=False)
    generic_point_name = db.Column(db.String(80), nullable=False)

    @validates('generic_point_uuid')
    def validate_generic_point_uuid(self, _, value):
        response: Response = gw_request(f'/ps/api/generic/points/uuid/{value}')
        if response.status_code != 200:
            raise ValueError(f'generic_point_uuid = {value}, does not exist')
        return value

    @validates('generic_point_name')
    def validate_generic_point_name(self, _, value):
        if not value:
            raise ValueError('generic_point_name should not be null or blank')
        return value

    @validates('bacnet_point_name')
    def validate_bacnet_point_name(self, _, value):
        if not value:
            raise ValueError('bacnet_point_name should not be null or blank')
        return value

    @classmethod
    def find_by_pagination(cls, page: int, per_page: int, sort: str, sort_by: str, search: str):
        query = cls.query
        if search:
            condition = or_(*[cls.bacnet_point_name.ilike(f'%{search}%'), cls.generic_point_name.ilike(f'%{search}%')])
            query = query.filter(condition)
        if sort or sort_by:
            if not sort_by:
                sort_by = cls.__table__.primary_key.columns.keys()[0]
            else:
                if sort_by not in cls.__table__.columns.keys():
                    raise ValueError(f"Does not exist sort_by{sort_by}")
            sort = desc(sort_by) if sort == "desc" else asc(sort_by)
            query = query.order_by(sort)
        return query.paginate(page=page, per_page=per_page or 50, error_out=False)

    @classmethod
    def find_by_bacnet_point_uuid(cls, bacnet_point_uuid):
        return cls.query.filter_by(bacnet_point_uuid=bacnet_point_uuid).first()

    @classmethod
    def find_by_generic_point_uuid(cls, generic_point_uuid):
        return cls.query.filter_by(generic_point_uuid=generic_point_uuid).first()
