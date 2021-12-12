from app import db
from .models import PoDataTime, Ops, Region, OpsData
from .google_sheet_logical import (
    data_from_ops,
    data_from_podata_time,
    data_from_uncommon_data,
    data_from_southwest_data,
    data_from_first_choice,
)
from typing import Type, Callable


def _fill_db(model: Type[db.Model], constructor: Callable, getter: Callable):
    if model != OpsData:
        if len(model.query.all()):
            db.session.query(model).delete()
            db.session.commit()
    values = getter
    for data in values:
        obj = model(**constructor(data))
        db.session.add(obj)
    db.session.commit()


def fill_ops():
    constructor = lambda data: dict(buyer=data[0], sku=int(data[1]), ingredient=data[2])
    getter = data_from_ops()
    return _fill_db(Ops, constructor, getter)


def fill_podata_time():
    constructor = lambda data: dict(
        total_quantity=int(data[0][0]),
        mid_sku=int(data[1][0]),
        destination=data[2][0] if len(data[2]) > 0 else " ",
        origin=data[3][0] if len(data[3]) > 0 else " ",
    )
    getter = data_from_podata_time()
    return _fill_db(PoDataTime, constructor, getter)


def fill_ops_data():
    if len(OpsData.query.all()) == 0:
        # first_choice
        region_fc_id = Region.query.filter_by(name="FirstChoice").first()
        constructor_fc = lambda data: dict(
            sku=int(data[0][0]), total_units=int(data[1][0]), region=region_fc_id
        )
        getter_fc = data_from_first_choice()
        _fill_db(OpsData, constructor_fc, getter_fc)
        # uncommon
        region_uc_id = Region.query.filter_by(name="UnСommon").first()
        constructor_uc = lambda data: dict(
            sku=int(data[0][0]), total_units=int(data[1][0]), region=region_uc_id
        )
        getter_uc = data_from_uncommon_data()
        _fill_db(OpsData, constructor_uc, getter_uc)
        # southwest
        region_sw_id = Region.query.filter_by(name="Southwest").first()
        constructor_sw = lambda data: dict(
            sku=0 if len(data[0]) == 0 or not data[0][0].isdigit() else int(data[0][0]),
            total_units=0
            if len(data[1]) == 0 or not data[1][0].isdigit()
            else int(data[1][0]),
            region=region_sw_id,
        )
        getter_sw = data_from_southwest_data()
        _fill_db(OpsData, constructor_sw, getter_sw)
    else:
        db.session.query(OpsData).delete()
        db.session.commit()
        return fill_ops_data()
