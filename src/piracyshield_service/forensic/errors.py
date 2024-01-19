
class ForensicErrorCode:

    GENERIC = '9001'

    ARCHIVE_NAME = '9002'

    HASH_TYPE_NOT_SUPPORTED = '9003'

    HASH_STRING_EMPTY = '9004'

    HASH_STRING_NON_VALID = '9005'

    HASH_STRING_EXISTS = '9006'

    NO_HASH_FOR_TICKET = '9007'

class ForensicErrorMessage:

    GENERIC = 'Error during the handling of the forensic evidence.'

    ARCHIVE_NAME = 'The archive name contains non valid characters.'

    HASH_TYPE_NOT_SUPPORTED = 'Forensic hash type not supported.'

    HASH_STRING_EMPTY = 'Forensic evidence hash not found.'

    HASH_STRING_NON_VALID = 'Forensic evidence hash non valid.'

    HASH_STRING_EXISTS = 'The hash string value is already present, meaning that this forensic evidence archive has already been submitted.'

    NO_HASH_FOR_TICKET = 'This ticket does not have any forensic evidence hash.'
