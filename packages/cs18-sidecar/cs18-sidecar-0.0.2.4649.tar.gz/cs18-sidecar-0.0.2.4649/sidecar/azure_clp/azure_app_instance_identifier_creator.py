from logging import Logger

from sidecar.app_instance_identifier import AppInstanceIdentifier
from sidecar.app_instance_identifier_creator import IAppInstanceIdentifierCreator


class AzureAppInstanceIdentifierCreator(IAppInstanceIdentifierCreator):
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger=logger)

    def create(self, app_name: str, instance_id: str) -> AppInstanceIdentifier:
        if not instance_id:
            raise Exception("Empty instance_id was provided")
        return AppInstanceIdentifier(name=app_name, infra_id=instance_id)
