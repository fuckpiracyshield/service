
class TicketErrorCode:

    GENERIC = '4000'

    NO_DATA = '4001'

    NON_VALID_TICKET_IDENTIFIER = '4002'

    MISSING_DDA_IDENTIFIER = '4003'

    NON_VALID_DDA_IDENTIFIER = '4004'

    UNKNOWN_DDA_IDENTIFIER = '4005'

    NON_VALID_DESCRIPTION = '4006'

    MISSING_FQDN = '4007'

    NON_VALID_FQDN = '4008'

    MISSING_IPV4 = '4009'

    NON_VALID_IPV4 = '4010'

    MISSING_IPV6 = '4011'

    NON_VALID_IPV6 = '4012'

    NON_VALID_ASSIGNED_TO = '4013'

    NON_EXISTENT_ASSIGNED_TO = '4014'

    REVOKE_TIME_EXCEEDED = '4015'

    REPORT_ERROR_TIME_EXCEEDED = '4016'

    TICKET_NOT_FOUND = '4017'

class TicketErrorMessage:

    GENERIC = 'Error during the handling of the ticket.'

    NO_DATA = 'No data provided.'

    NON_VALID_TICKET_IDENTIFIER = 'Non valid ticket identifier.'

    MISSING_DDA_IDENTIFIER = 'Missing DDA identifier.'

    NON_VALID_DDA_IDENTIFIER = 'Non valid DDA identifier.'

    UNKNOWN_DDA_IDENTIFIER = 'The DDA identifier does not exist or not assigned to this account.'

    NON_VALID_DESCRIPTION = 'The description should be a string between 3 and 255 characters.'

    MISSING_FQDN = 'Missing FQDN list.'

    NON_VALID_FQDN = 'Non valid FQDN.'

    MISSING_IPV4 = 'Missing IPv4 list.'

    NON_VALID_IPV4 = 'Non valid IPv4.'

    MISSING_IPV6 = 'Missing IPv6 list.'

    NON_VALID_IPV6 = 'Non valid IPv6.'

    NON_VALID_ASSIGNED_TO = 'Non valid assigned identifier.'

    NON_EXISTENT_ASSIGNED_TO = 'One or more providers indicated in `assigned_to` does not exist.'

    REVOKE_TIME_EXCEEDED = 'Cannot remove the ticket, exceeded max revoke time.'

    REPORT_ERROR_TIME_EXCEEDED = 'Cannot create the ticket, exceeded max error reporting time.'

    TICKET_NOT_FOUND = 'Ticket not found.'
