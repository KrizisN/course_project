from .models import OpsData, PoDataTime


def calculate_business_logic(reg_db, ops):
    dictionary = {}
    for reg in reg_db:
        objs_inhouse = (
            OpsData.query.filter(OpsData.sku == ops.sku)
            .filter(OpsData.region_id == reg.id)
            .all()
        )
        inhouse = 0
        outbound = 0
        inbound = 0
        for obj in objs_inhouse:
            inhouse += obj.total_units
        objs_inbound = PoDataTime.query.filter(PoDataTime.mid_sku == ops.sku).filter(
            PoDataTime.destination == reg.name
        )
        objs_outbound = PoDataTime.query.filter(PoDataTime.mid_sku == ops.sku).filter(
            PoDataTime.origin == reg.name
        )
        for obj in objs_inbound:
            inbound += obj.total_quantity
        for obj in objs_outbound:
            outbound += obj.total_quantity
        dictionary[reg.name] = {
            "inHouse": inhouse,
            "outbound": outbound,
            "inbound": inbound,
        }
    return dictionary
