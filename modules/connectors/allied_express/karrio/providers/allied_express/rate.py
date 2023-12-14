import karrio.schemas.allied_express.rate_request as allied
import karrio.schemas.allied_express.rate_response as rating
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.allied_express.error as error
import karrio.providers.allied_express.utils as provider_utils
import karrio.providers.allied_express.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[provider_utils.AlliedResponse],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate.data["result"], settings)
        for rate in [response]
        if not rate.is_error and "result" in (rate.data or {})
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(rating.ResultType, data)
    service = provider_units.ShippingService.allied_standard
    charges = [
        ("Job charge", lib.to_money(rate.jobCharge)),
        *((s.chargeCode, lib.to_money(s.netValue)) for s in rate.surcharges),
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name,
        total_charge=lib.to_money(rate.totalCharge),
        currency=units.Currency.AUD.name,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=amount,
                currency=units.Currency.AUD.name,
            )
            for name, amount in charges
            if amount > 0
        ],
        meta=dict(
            service_name=service.name,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = lib.to_services(payload.services, provider_units.ShippingService).first
    options = lib.to_shipping_options(
        payload.options,
        option_type=provider_units.ShippingOption,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    request = allied.RateRequestType(
        bookedBy=shipper.contact,
        account=settings.account,
        instructions=options.instructions.state,
        itemCount=len(packages),
        items=[
            allied.ItemType(
                dangerous=pkg.options.dangerous_good.state,
                height=pkg.height.CM,
                length=pkg.length.CM,
                width=pkg.width.CM,
                weight=pkg.weight.KG,
                volume=pkg.volume.value,
                itemCount=(pkg.items.quantity if any(pkg.items) else 1),
            )
            for pkg in packages
        ],
        jobStopsP=allied.JobStopsType(
            companyName=shipper.company_name,
            contact=shipper.contact,
            emailAddress=shipper.email,
            geographicAddress=allied.GeographicAddressType(
                address1=shipper.address_line1,
                address2=shipper.address_line2,
                country=shipper.country_code,
                postCode=shipper.postal_code,
                state=shipper.state_code,
                suburb=shipper.city,
            ),
            phoneNumber=shipper.phone_number,
        ),
        jobStopsD=allied.JobStopsType(
            companyName=recipient.company_name,
            contact=recipient.contact,
            emailAddress=recipient.email,
            geographicAddress=allied.GeographicAddressType(
                address1=recipient.address_line1,
                address2=recipient.address_line2,
                country=recipient.country_code,
                postCode=recipient.postal_code,
                state=recipient.state_code,
                suburb=recipient.city,
            ),
            phoneNumber=recipient.phone_number,
        ),
        referenceNumbers=(
            [payload.reference] if any(payload.reference or "") else None
        ),
        serviceLevel=(service.value if service else "R"),
        weight=packages.weight.KG,
        volume=packages.volume,
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_json(_)
        .replace("jobStopsP", "jobStops_P")
        .replace("jobStopsD", "jobStops_D"),
    )
