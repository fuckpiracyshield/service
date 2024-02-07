
class ForensicErrorCode:

    GENERIC = '9000'

    ARCHIVE_NAME = '9001'

    HASH_TYPE_NOT_SUPPORTED = '9002'

    HASH_STRING_EMPTY = '9003'

    HASH_STRING_NON_VALID = '9004'

    NO_HASH_FOR_TICKET = '9005'

    EXTENSION_NOT_SUPPORTED = '9006'

class ForensicErrorMessage:

    # error during the handling of the forensic evidence
    GENERIC = 'Generic error.'

    ARCHIVE_NAME = 'The archive name contains non valid characters.'

    HASH_TYPE_NOT_SUPPORTED = 'Forensic hash type not supported.'

    HASH_STRING_EMPTY = 'Forensic evidence hash not found.'

    HASH_STRING_NON_VALID = 'Forensic evidence hash non valid.'

    NO_HASH_FOR_TICKET = 'This ticket does not have any forensic evidence hash.'

    EXTENSION_NOT_SUPPORTED = 'The file extension is not supported.'
