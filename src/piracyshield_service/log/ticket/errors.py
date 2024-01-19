
class LogTicketErrorCode:

    GENERIC = '5101'

    MISSING_TICKET_ID = '5102'

    NON_VALID_TICKET_ID = '5103'

    MISSING_MESSAGE = '5104'

    NON_VALID_MESSAGE = '5105'

    CANNOT_REMOVE = '5106'

class LogTicketErrorMessage:

    GENERIC = 'Generic error.'

    MISSING_TICKET_ID = 'Missing ticket identifier.'

    NON_VALID_TICKET_ID = 'Non valid ticket identifier.'

    MISSING_MESSAGE = 'Missing message.'

    NON_VALID_MESSAGE = 'Non valid message.'

    CANNOT_REMOVE = 'The items could not be removed. Ensure you have proper permissions to perform this operation.'
