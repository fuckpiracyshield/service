
class WhitelistErrorCode:

    GENERIC = '6000'

    NON_VALID_GENRE = '6001'

    MISSING_FQDN = '6002'

    NON_VALID_FQDN = '6003'

    MISSING_IPV4 = '6004'

    NON_VALID_IPV4 = '6005'

    MISSING_IPV6 = '6006'

    NON_VALID_IPV6 = '6007'

    MISSING_REGISTRAR = '6008'

    NON_VALID_REGISTRAR = '6009'

    MISSING_AS_CODE = '6010'

    NON_VALID_AS_CODE = '6011'

    ITEM_EXISTS = '6012'

    ITEM_HAS_TICKET = '6013'

    CANNOT_REMOVE = '6014'

    CANNOT_SET_STATUS = '6015'

class WhitelistErrorMessage:

    GENERIC = 'Error during the creation of the whitelist item.'

    NON_VALID_GENRE = 'Non valid genre.'

    MISSING_FQDN = 'Missing FQDN item.'

    NON_VALID_FQDN = 'Non valid FQDN.'

    MISSING_IPV4 = 'Missing IPv4 item.'

    NON_VALID_IPV4 = 'Non valid IPv4.'

    MISSING_IPV6 = 'Missing IPv6 item.'

    NON_VALID_IPV6 = 'Non valid IPv6.'

    MISSING_REGISTRAR = 'Missing registrar.'

    NON_VALID_REGISTRAR = 'Non valid registrar. A registrar must be a string (allowed characters: ` -`)'

    MISSING_AS_CODE = 'Missing AS code.'

    NON_VALID_AS_CODE = 'Non valid AS code. An AS code must be represented by a sequence of maximum 9 numbers with or without the `AS` prefix.'

    ITEM_EXISTS = 'This item has been already created.'

    ITEM_HAS_TICKET = 'This item is in a ticket and cannot be whitelisted.'

    CANNOT_REMOVE = 'The item could not be removed. Ensure you have proper permissions or to specify a valid item.'

    CANNOT_SET_STATUS = 'Cannot update the status of the whitelist item.'
