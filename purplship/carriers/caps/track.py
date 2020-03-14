from typing import Tuple, List
from pycaps.track import pin_summary
from purplship.core.settings import Settings
from purplship.core.utils.xml import Element
from purplship.core.utils.serializable import Serializable
from purplship.core.models import TrackingRequest, TrackingDetails, TrackingEvent, Error
from purplship.carriers.caps.error import parse_error_response


def parse_tracking_summary(
    response: Element, settings: Settings
) -> Tuple[List[TrackingDetails], List[Error]]:
    pin_summaries = response.xpath(".//*[local-name() = $name]", name="pin-summary")
    tracking: List[TrackingDetails] = [
        _extract_tracking(pin, settings) for pin in pin_summaries
    ]
    return tracking, parse_error_response(response, settings)


def _extract_tracking(pin_summary_node: Element, settings: Settings) -> TrackingDetails:
    pin_summary_ = pin_summary()
    pin_summary_.build(pin_summary_node)
    return TrackingDetails(
        carrier=settings.carrier_name,
        tracking_number=pin_summary_.pin,
        shipment_date=str(pin_summary_.mailed_on_date),
        events=[
            TrackingEvent(
                date=str(pin_summary_.event_date_time),
                signatory=pin_summary_.signatory_name,
                code=pin_summary_.event_type,
                location=pin_summary_.event_location,
                description=pin_summary_.event_description,
            )
        ],
    )


def tracking_pins_request(payload: TrackingRequest) -> Serializable[List[str]]:
    return Serializable(payload.tracking_numbers)
