"""PurplShip Australia post client settings."""

import attr
from purplship.carriers.aups.utils import Settings as BaseSettings


@attr.s(auto_attribs=True)
class Settings(BaseSettings):
    """Australia post connection settings."""

    api_key: str
    password: str
    account_number: str
    carrier_name: str = "Australia Post Shipping"
    server_url: str = "https://digitalapi.auspost.com.au"
