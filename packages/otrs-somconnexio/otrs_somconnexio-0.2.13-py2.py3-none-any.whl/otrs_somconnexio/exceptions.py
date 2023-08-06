class OTRSClientException(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)
        self.message = message


class ErrorCreatingSession(OTRSClientException):
    pass


class TicketNotCreated(OTRSClientException):
    pass


class TicketNotFoundError(OTRSClientException):
    pass


class OTRSIntegrationUnknownError(OTRSClientException):
    pass


class UserManagementResponseEmpty(OTRSClientException):
    def __init__(self, user_id, call):
        message = "Error in method {} from user {}".format(call, user_id)
        super(OTRSClientException, self).__init__(message)
