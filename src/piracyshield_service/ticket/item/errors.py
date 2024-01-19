
class TicketItemErrorCode:

    GENERIC = '5000'

    TICKET_ITEM_NOT_FOUND = '5001'

    TICKET_ITEM_PROVIDER_ID_MISSING = '5002'

    TICKET_ITEM_PROVIDER_ID_NON_VALID = '5003'

    TICKET_ITEM_VALUE_MISSING = '5004'

    TICKET_ITEM_VALUE_NON_VALID = '5005'

    TICKET_ITEM_TIMESTAMP_NON_VALID = '5006'

    TICKET_ITEM_NOTE_NON_VALID = '5007'

    TICKET_ITEM_REASON_MISSING = '5008'

    TICKET_ITEM_REASON_NON_VALID = '5009'

    TICKET_ITEM_UPDATE_TIME_EXCEEDED = '5010'

class TicketItemErrorMessage:

    GENERIC = 'Error during the creation of the ticket item.'

    TICKET_ITEM_NOT_FOUND = 'Ticket item not found.'

    TICKET_ITEM_PROVIDER_ID_MISSING = 'Missing provider identifier.'

    TICKET_ITEM_PROVIDER_ID_NON_VALID = 'Non valid provider identifier.'

    TICKET_ITEM_VALUE_MISSING = 'Missing ticket item value.'

    TICKET_ITEM_VALUE_NON_VALID = 'Non valid ticket item value.'

    TICKET_ITEM_TIMESTAMP_NON_VALID = 'Non valid timestamp.'

    TICKET_ITEM_NOTE_NON_VALID = 'Non valid note.'

    TICKET_ITEM_REASON_MISSING = 'Missing unprocessed reason.'

    TICKET_ITEM_REASON_NON_VALID = 'Non valid unprocessed reason.'

    TICKET_ITEM_UPDATE_TIME_EXCEEDED = 'Cannot update the ticket item: max update time has been exceeded.'
