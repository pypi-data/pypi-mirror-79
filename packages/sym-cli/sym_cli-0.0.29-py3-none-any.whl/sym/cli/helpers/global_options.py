import sys
from dataclasses import dataclass, field
from typing import ClassVar, Mapping, Optional, Type

from ..helpers import segment
from ..saml_clients.chooser import choose_saml_client


@dataclass
class GlobalOptions:
    saml_client_type: Type["SAMLClient"] = field(
        default_factory=lambda: choose_saml_client("auto")
    )
    saml_clients: Mapping[str, "SAMLClient"] = field(default_factory=dict)

    debug: bool = False
    log_dir: Optional[str] = None

    def dprint(self, s: str):
        if self.debug:
            print(f"{s}\n", file=sys.stderr)

    def create_saml_client(self, resource: str) -> "SAMLClient":
        segment.track("Resource Requested", resource=resource)
        if resource not in self.saml_clients:
            self.saml_clients[resource] = self.saml_client_type(resource, options=self)
        return self.saml_clients[resource]

    def to_dict(self):
        return {"debug": self.debug, "saml_client": self.saml_client_type.__name__}
