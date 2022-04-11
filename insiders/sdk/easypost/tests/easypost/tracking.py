import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Tracking
from karrio.core.models import TrackingRequest
from tests.easypost.fixture import gateway


class TestEasyPostTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(**TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("karrio.mappers.easypost.proxy.http") as mock:
            mock.return_value = "{}"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/trackers",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.easypost.proxy.http") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(DP.to_dict(parsed_response))
            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedTrackingResponse)
            )

    def test_parse_error_response(self):
        with patch("karrio.mappers.easypost.proxy.http") as mock:
            mock.return_value = ErrorResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(ParsedErrorResponse)
            )


if __name__ == "__main__":
    unittest.main()


TRACKING_PAYLOAD = {
    "tracking_numbers": ["EZ1000000001"],
    "options": {"carrier": "usps"},
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "easypost",
            "carrier_name": "easypost",
            "delivered": False,
            "events": [
                {
                    "code": "pre_transit",
                    "date": "2022-03-11",
                    "description": "Pre-Shipment Info Sent to USPS",
                    "time": "03:34",
                },
                {
                    "code": "pre_transit",
                    "date": "2022-03-11",
                    "description": "Shipping Label Created",
                    "location": "HOUSTON, TX, 77063",
                    "time": "16:11",
                },
            ],
            "tracking_number": "EZ1000000001",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "easypost",
            "carrier_name": "easypost",
            "code": "TRACKER.CREATE.ERROR",
            "details": {"tracking_number": "EZ1000000001"},
            "message": "In test mode, only test tracking numbers are valid. Test tracking numbers are EZ1000000001, EZ2000000002, ... , EZ7000000007",
        }
    ],
]


TrackingRequestJSON = [{"carrier": "usps", "tracking_code": "EZ1000000001"}]

TrackingResponseJSON = """{
	"id": "trk_eb692ebb773d40619dfc0417d2bb26c2",
	"object": "Tracker",
	"mode": "test",
	"tracking_code": "EZ1000000001",
	"status": "pre_transit",
	"status_detail": "status_update",
	"created_at": "2022-04-11T03:34:58Z",
	"updated_at": "2022-04-11T03:34:58Z",
	"signed_by": null,
	"weight": null,
	"est_delivery_date": "2022-04-11T03:34:58Z",
	"shipment_id": null,
	"carrier": "USPS",
	"tracking_details": [
		{
			"object": "TrackingDetail",
			"message": "Pre-Shipment Info Sent to USPS",
			"description": null,
			"status": "pre_transit",
			"status_detail": "status_update",
			"datetime": "2022-03-11T03:34:58Z",
			"source": "USPS",
			"carrier_code": null,
			"tracking_location": {
				"object": "TrackingLocation",
				"city": null,
				"state": null,
				"country": null,
				"zip": null
			}
		},
		{
			"object": "TrackingDetail",
			"message": "Shipping Label Created",
			"description": null,
			"status": "pre_transit",
			"status_detail": "status_update",
			"datetime": "2022-03-11T16:11:58Z",
			"source": "USPS",
			"carrier_code": null,
			"tracking_location": {
				"object": "TrackingLocation",
				"city": "HOUSTON",
				"state": "TX",
				"country": null,
				"zip": "77063"
			}
		}
	],
	"carrier_detail": {
		"object": "CarrierDetail",
		"service": "First-Class Package Service",
		"container_type": null,
		"est_delivery_date_local": null,
		"est_delivery_time_local": null,
		"origin_location": "HOUSTON TX, 77001",
		"origin_tracking_location": {
			"object": "TrackingLocation",
			"city": "HOUSTON",
			"state": "TX",
			"country": null,
			"zip": "77063"
		},
		"destination_location": "CHARLESTON SC, 29401",
		"destination_tracking_location": null,
		"guaranteed_delivery_date": null,
		"alternate_identifier": null,
		"initial_delivery_attempt": null
	},
	"finalized": true,
	"is_return": false,
	"public_url": "https://track.easypost.com/djE6dHJrX2ViNjkyZWJiNzczZDQwNjE5ZGZjMDQxN2QyYmIyNmMy",
	"fees": [
		{
			"object": "Fee",
			"type": "TrackerFee",
			"amount": "0.02000",
			"charged": false,
			"refunded": false
		}
	]
}
"""

ErrorResponseJSON = """{
	"error": {
		"code": "TRACKER.CREATE.ERROR",
		"message": "In test mode, only test tracking numbers are valid. Test tracking numbers are EZ1000000001, EZ2000000002, ... , EZ7000000007",
		"errors": []
	}
}
"""
