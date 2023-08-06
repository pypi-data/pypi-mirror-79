# coding: utf-8
import unittest
from mock import Mock, patch

from otrs_somconnexio.otrs_models.mobile_ticket import MobileTicket
from otrs_somconnexio.otrs_models.configurations.mobile_ticket import MobileTicketConfiguration
from otrs_somconnexio.ticket_exceptions import CustomerMailMissing, CustomerUserMissing


class MobileTicketTestCase(unittest.TestCase):

    @patch('otrs_somconnexio.otrs_models.mobile_ticket.Ticket')
    def test_build_ticket(self, MockTicket):
        party = Mock(spec=[
            'get_contact_email',
            'get_identifier',
            'get_contact_phone'
        ])
        email = Mock(spec=['value'])
        email.value = 'contact@mail.com'
        party.get_contact_email.return_value = email
        vat = Mock(spec=['code'])
        vat.code = 'VatCode'
        party.get_identifier.return_value = vat
        phone = Mock(spec=['value'])
        phone.value = '666666666'
        party.get_contact_phone.return_value = phone

        eticom_contract = Mock(spec=[
            'id',
            'party'
        ])
        eticom_contract.id = 123
        eticom_contract.party = party

        expected_ticket_arguments = {
            "Title": "Sol·licitud mobile {}".format(eticom_contract.id),
            "Type": MobileTicketConfiguration.type,
            "Queue": MobileTicketConfiguration.queue,
            "State": MobileTicketConfiguration.state,
            "Priority": MobileTicketConfiguration.priority,
            "CustomerUser": 'contact@mail.com',
            "CustomerID": 'contact@mail.com'
        }

        MobileTicket(eticom_contract)._build_ticket()
        MockTicket.assert_called_with(expected_ticket_arguments)

    @patch('otrs_somconnexio.otrs_models.mobile_ticket.Ticket')
    def test_build_ticket_raise_CustomerMailMissing_error(self, MockTicket):
        party = Mock(spec=[
            'get_contact_email'
        ])
        party.get_contact_email.return_value = None

        eticom_contract = Mock(spec=[
            'id',
            'party'
        ])
        eticom_contract.id = 123
        eticom_contract.party = party

        with self.assertRaises(CustomerMailMissing):
            MobileTicket(eticom_contract)._build_ticket()

    @patch('otrs_somconnexio.otrs_models.mobile_ticket.Ticket')
    def test_build_ticket_raise_CustomerUserMissing_error(self, MockTicket):
        eticom_contract = Mock(spec=[
            'id',
            'party'
        ])
        eticom_contract.id = 123
        eticom_contract.party = None

        with self.assertRaises(CustomerUserMissing):
            MobileTicket(eticom_contract)._build_ticket()

    @patch('otrs_somconnexio.otrs_models.mobile_ticket.MobileArticle')
    def test_build_article(self, MockMobileArticle):
        eticom_contract = Mock(spec=['id'])
        eticom_contract.id = 123

        mock_mobile_article = MockMobileArticle.return_value

        MobileTicket(eticom_contract)._build_article()

        MockMobileArticle.assert_called_with('mobile', eticom_contract)
        mock_mobile_article.call.assert_called_once()

    @patch('otrs_somconnexio.otrs_models.mobile_ticket.MobileDynamicFields')
    def test_build_dynamic_fields(self, MockMobileDynamicFields):
        eticom_contract = Mock(spec=[])

        mock_mobile_dynamic_fields = MockMobileDynamicFields.return_value

        MobileTicket(eticom_contract)._build_dynamic_fields()

        MockMobileDynamicFields.assert_called_with(
            eticom_contract,
            MobileTicketConfiguration.process_id,
            MobileTicketConfiguration.activity_id,
        )
        mock_mobile_dynamic_fields.all.assert_called_once()

    @patch('otrs_somconnexio.otrs_models.mobile_ticket.OTRSClient')
    def test_create(self, MockOTRSClient):
        eticom_contract = Mock(spec=[
            'id',
            'party'
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
        eticom_contract.party = Mock(spec=[
            'get_identifier',
            'get_contact_email',
            'get_contact_phone',
            'first_name',
            'name',
        ])
        eticom_contract.mobile_phone_number = "666666666"
        eticom_contract.mobile_option = "new"
        eticom_contract.mobile_min = "0"
        eticom_contract.bank_iban_service = "ES6621000418401234567891"

        mock_otrs_client = Mock(spec=['create_otrs_process_ticket'])
        mock_otrs_client.create_otrs_process_ticket.return_value = Mock(MobileTicket, autospec=True)
        mock_otrs_client.create_otrs_process_ticket.return_value.id = 123
        mock_otrs_client.create_otrs_process_ticket.return_value.number = '#123'
        MockOTRSClient.return_value = mock_otrs_client

        ticket = MobileTicket(eticom_contract)
        ticket.create()

        MockOTRSClient.assert_called_once_with()
        mock_otrs_client.create_otrs_process_ticket.assert_called_once()

        self.assertEqual(ticket.id, 123)
        self.assertEqual(ticket.number, '#123')
