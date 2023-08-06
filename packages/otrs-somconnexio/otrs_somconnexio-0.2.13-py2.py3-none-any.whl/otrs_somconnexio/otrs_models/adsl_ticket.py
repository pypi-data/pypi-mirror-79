# coding: utf-8
from otrs_somconnexio.otrs_models.internet_ticket import InternetTicket
from otrs_somconnexio.otrs_models.adsl_dynamic_fields import ADSLDynamicFields
from otrs_somconnexio.otrs_models.configurations.adsl_ticket import ADSLTicketConfiguration


class ADSLTicket(InternetTicket):

    def __init__(self, econtract, otrs_configuration=None):
        self.eticom_contract = econtract
        self.otrs_configuration = ADSLTicketConfiguration(otrs_configuration)

    def service_type(self):
        return 'adsl'

    def _build_dynamic_fields(self):
        return ADSLDynamicFields(
            self.eticom_contract,
            self._ticket_process_id(),
            self._ticket_activity_id()
        ).all()

    def _ticket_type(self):
        return self.otrs_configuration.type

    def _ticket_queue(self):
        return self.otrs_configuration.queue

    def _ticket_state(self):
        return self.otrs_configuration.state

    def _ticket_priority(self):
        return self.otrs_configuration.priority

    def _ticket_activity_id(self):
        return self.otrs_configuration.activity_id

    def _ticket_process_id(self):
        return self.otrs_configuration.process_id
