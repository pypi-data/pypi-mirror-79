"""DNS Authenticator for transip api."""
import logging

import zope.interface

from certbot import interfaces
from certbot.plugins import dns_common

from transip.service.domain import DomainService
from transip.service.objects import DnsEntry, Domain

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for transip api

    This Authenticator uses the transip Remote REST API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using transip for DNS)."
    ttl = 60

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.username = None
        self.apikey = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=120
        )
        add("credentials", help="transip credentials INI file.")

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "transip credentials INI file",
            {
                "username": "Username for transip Remote API.",
                "api-key-file": "Password for transip Remote API.",
            },
        )

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the transip Remote REST API."
        )

    def _perform(self, domain, validation_name, validation):
        dns_entry = self._get_dns_entry(domain, validation_name, validation)
        self._get_transip_client().add_dns_entries(domain, [dns_entry])

    def _cleanup(self, domain, validation_name, validation):
        dns_entry = self._get_dns_entry(domain, validation_name, validation)
        self._get_transip_client().remove_dns_entries(domain, [dns_entry])

    def _get_dns_entry(self, domain, validation_name, validation):
        # transip api expects the name record without the domain part at the end
        if validation_name.endswith(domain):
            validation_name = validation.name[:-len(domain)].strip('.')
        return DnsEntry(validation_name, self.ttl, 'TXT', validation)

    def _get_transip_client(self):
        return DomainService(
            self.credentials.conf("username"),
            private_key_file=self.credentials.conf("api-key-file"),
        )
