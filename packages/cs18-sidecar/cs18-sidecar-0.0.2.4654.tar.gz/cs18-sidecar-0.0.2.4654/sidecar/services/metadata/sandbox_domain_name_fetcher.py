from sidecar.services.metadata.sandbox_public_address_fetcher import SandboxMetadataFetcher


class SandboxDomainNameFetcher(SandboxMetadataFetcher):
    def __init__(self, sandbox_id: str) -> None:
        super().__init__()
        self._sandbox_id = sandbox_id

    def get_value(self) -> str:
        return f'{self._sandbox_id}.sandbox.com'


class KubSandboxDomainNameFetcher(SandboxDomainNameFetcher):
    def get_value(self) -> str:
        return "unsupported-feature-for-k8s"
