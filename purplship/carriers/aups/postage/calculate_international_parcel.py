from purplship.core.models import RateRequest
from purplship.core.units import WeightUnit, Weight
from pyaups.international_parcel_postage import ServiceRequest


def calculate_international_parcel_request(payload: RateRequest) -> ServiceRequest:
    weight_unit: WeightUnit = WeightUnit[payload.parcel.weight_unit or "KG"]
    request = ServiceRequest(
        country_code=payload.recipient.country_code,
        weight=Weight(payload.parcel.weight, weight_unit).KG,
    )
    return request
