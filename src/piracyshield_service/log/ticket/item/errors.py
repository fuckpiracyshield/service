
class LogTicketItemErrorCode:

    GENERIC = '5201'

    MISSING_TICKET_ID = '5202'

    NON_VALID_TICKET_ID = '5203'

    MISSING_MESSAGE = '5204'

    NON_VALID_MESSAGE = '5205'

    CANNOT_REMOVE = '5206'

class LogTicketItemErrorMessage:

    GENERIC = 'Generic error.'

    MISSING_TICKET_ITEM_ID = 'Missing ticket item identifier.'

    NON_VALID_TICKET_ITEM_ID = 'Non valid ticket item identifier.'

    MISSING_MESSAGE = 'Missing message.'

    NON_VALID_MESSAGE = 'Non valid message.'

    CANNOT_REMOVE = 'The items could not be removed. Ensure you have proper permissions to perform this operation.'
