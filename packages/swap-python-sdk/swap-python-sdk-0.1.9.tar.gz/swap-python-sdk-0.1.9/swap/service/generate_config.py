from os import path
from uuid import uuid4
import requests
import json
from swap.common.config import Settings
from dataclasses import dataclass
from swap.common.logging import logger


@dataclass(frozen=True)
class Config:
    subscription: str
    catalogue_uuid: str
    name: str
    service_description: str
    service_provider_signature: str
    service_provider_uuid: str
    parameters: str
    project: str = 'microservice-pilot'
    topic: str = 'akerbp-stage-pre-seismic-processing'
    dataset_type: str = 'SEGY'
    service_provider_name: str = 'AkerBP'
    icon_base64: str = 'ICON_BASE64'
    icon_url: str = 'https://ui.dev.swap.akerbp.com/static/media/Skua-salt-2010.4fa0f606.jpg'


class ConfigGenerator:
    def __init__(self, config_output_path, parameters):
        self.config_output_path = config_output_path
        self.parameters = parameters
        self.swap_api_token = Settings.SWAP_API_TOKEN

    def get_subscription(self) -> str:
        subscription_generation_url = 'https://ubl.stage.swap.akerbp.com/template_app/subscription'
        response = requests.get(subscription_generation_url,
                                params={
                                    "api_key": self.swap_api_token
                                })

        response_as_dict = json.loads(response.text)
        logger.debug(response_as_dict)
        new_subscription_id = response_as_dict['subscription_id']

        return new_subscription_id

    def get_name(self) -> str:
        name = input('Enter a name for your service: ')
        return name + '_dev'

    def get_description(self) -> str:
        return input('Enter a description for your service: ')

    def create_config(self) -> Config:
        return Config(
            subscription=self.get_subscription(),
            catalogue_uuid=f"{uuid4()}",
            name=self.get_name(),
            service_description=self.get_description(),
            service_provider_signature=f"{uuid4()}",
            service_provider_uuid=f"{uuid4()}",
            parameters=self.parameters
        )

    def transpile(self) -> str:
        return ("from swap.messaging.models import Config\n"
               f"service_config = {self.create_config()}")

    def write(self):
        with open(self.config_output_path, 'w') as file:
            file.write(self.transpile())
        print(f'A new service config has been successfully written to {path.abspath(self.config_output_path)}')
