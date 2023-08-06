from typing import Dict, Optional

from sidecar.services.metadata.sandbox_domain_name_fetcher import SandboxDomainNameFetcher
from sidecar.services.metadata.sandbox_public_address_fetcher import SandboxPublicAddressFetcher


class BuiltInInputsProvider:
    def __init__(self, sandbox_id: str,
                 sandbox_domain_name_fetcher: SandboxDomainNameFetcher,
                 sandbox_public_address_fetcher: Optional[SandboxPublicAddressFetcher]):
        self._sandbox_id = sandbox_id
        self._sandbox_domain_name_fetcher = sandbox_domain_name_fetcher
        self._sandbox_public_address_fetcher = sandbox_public_address_fetcher

    def get_inputs(self) -> Dict[str, str]:
        domain_name = self._sandbox_domain_name_fetcher.get_value()

        try:
            sandbox_public_address = self._sandbox_public_address_fetcher.get_value() if self._sandbox_public_address_fetcher else ''
        except:
            sandbox_public_address = ''

        return {
            'DOMAIN_NAME': domain_name,
            'SANDBOX_ID': self._sandbox_id,
            'PUBLIC_ADDRESS': sandbox_public_address,
            'COLONY_DOMAIN_NAME': domain_name,
            'COLONY_SANDBOX_ID': self._sandbox_id,
            'COLONY_PUBLIC_ADDRESS': sandbox_public_address
        }