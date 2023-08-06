import unittest
from mock import Mock, patch

from otrs_somconnexio.otrs_models.ticket_factory import TicketFactory
from otrs_somconnexio.otrs_models.adsl_ticket import ADSLTicket
from otrs_somconnexio.otrs_models.fiber_ticket import FiberTicket
from otrs_somconnexio.otrs_models.mobile_ticket import MobileTicket


class TicketFactoryIntegrationTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.otrs_models.mobile_ticket.OTRSClient')
    def test_create_mobile_ticket_factory(self, MockOTRSClient):
        contract_type = 'mobile'

        party = Mock(spec=[
            'get_identifier',
            'get_contact_email',
            'get_contact_phone',
            'first_name',
            'name'
        ])

        eticom_contract = Mock(spec=[
            'id',
            'party',
            'bank_iban_service',
            'mobile_phone_number',
            'mobile_sc_icc',
            'mobile_icc_number',
            'mobile_min',
            'mobile_internet',
            'mobile_option',
            'mobile_telecom_company',
            'mobile_vat_number',
            'mobile_name',
            'mobile_surname',
        ])
        eticom_contract.id = 123
        eticom_contract.party = party
        eticom_contract.mobile_option = 'new'
        eticom_contract.mobile_min = '0'

        otrs_process_ticket = Mock(spec=['id'])
        otrs_process_ticket.id = 234

        mock_otrs_client = Mock(spec=['create_otrs_process_ticket'])
        mock_otrs_client.create_otrs_process_ticket.return_value = otrs_process_ticket
        MockOTRSClient.return_value = mock_otrs_client

        ticket = TicketFactory(contract_type, eticom_contract).build()
        ticket.create()

        self.assertEquals(ticket.id, 234)
        self.assertIsInstance(ticket, MobileTicket)

    @patch('otrs_somconnexio.otrs_models.internet_ticket.OTRSClient')
    def test_create_adsl_ticket_factory(self, MockOTRSClient):
        contract_type = 'adsl'
        eticom_contract = Mock(spec=[''])

        eticom_contract = Mock(spec=[
            'id',
            'party',
            'bank_iban_service',
            "internet_now",
            "internet_telecom_company",
            "internet_phone",
            "internet_phone_now",
            "internet_phone_minutes",
            "internet_phone_number",
            "internet_street",
            "internet_city",
            "internet_zip",
            "internet_subdivision",
            "internet_country",
            "internet_delivery_street",
            "internet_delivery_city",
            "internet_delivery_zip",
            "internet_delivery_subdivision",
            "internet_delivery_country",
            "internet_vat_number",
            "internet_name",
            "internet_surname",
            "internet_lastname",
            "notes",
            "coverage_availability",
            "change_address",
        ])

        otrs_process_ticket = Mock(spec=['id'])
        otrs_process_ticket.id = 234

        mock_otrs_client = Mock(spec=['create_otrs_process_ticket'])
        mock_otrs_client.create_otrs_process_ticket.return_value = otrs_process_ticket
        MockOTRSClient.return_value = mock_otrs_client

        ticket = TicketFactory(contract_type, eticom_contract).build()
        ticket.create()

        self.assertIsInstance(ticket, ADSLTicket)
        self.assertEquals(ticket.id, 234)

    @patch('otrs_somconnexio.otrs_models.internet_ticket.OTRSClient')
    def test_create_fiber_ticket_factory(self, MockOTRSClient):
        contract_type = 'fiber'

        eticom_contract = Mock(spec=[
            'id',
            'party',
            'bank_iban_service',
            "internet_now",
            "internet_telecom_company",
            "internet_phone",
            "internet_phone_now",
            "internet_phone_minutes",
            "internet_phone_number",
            "internet_street",
            "internet_city",
            "internet_zip",
            "internet_subdivision",
            "internet_country",
            "internet_delivery_street",
            "internet_delivery_city",
            "internet_delivery_zip",
            "internet_delivery_subdivision",
            "internet_delivery_country",
            "internet_vat_number",
            "internet_name",
            "internet_surname",
            "internet_lastname",
            "notes",
            "internet_speed",
            "coverage_availability",
            "change_address",
        ])

        otrs_process_ticket = Mock(spec=['id'])
        otrs_process_ticket.id = 234

        mock_otrs_client = Mock(spec=['create_otrs_process_ticket'])
        mock_otrs_client.create_otrs_process_ticket.return_value = otrs_process_ticket
        MockOTRSClient.return_value = mock_otrs_client

        ticket = TicketFactory(contract_type, eticom_contract).build()
        ticket.create()

        self.assertIsInstance(ticket, FiberTicket)
        self.assertEquals(ticket.id, 234)
