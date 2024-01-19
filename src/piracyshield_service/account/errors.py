
class AccountErrorCode:

    GENERIC = '3001'

    EMAIL_EXISTS = '3002'

    NAME_ERROR = '3003'

    EMAIL_ERROR = '3004'

    PASSWORD_ERROR = '3005'

    PASSWORD_MISMATCH_ERROR = '3006'

    ROLE_ERROR = '3007'

    FLAG_UNKNOWN = '3008'

    FLAG_NON_VALID_VALUE = '3009'

    FLAG_NOT_FOUND = '3010'

    ACCOUNT_NOT_FOUND = '3011'

    PASSWORD_CHANGE_NON_VALID = '3012'

    PASSWORD_CHANGE_MISMATCH = '3013'

    PASSWORD_DIFF = '3014'

class AccountErrorMessage:

    GENERIC = 'Error during the creation of the account.'

    EMAIL_EXISTS = 'The e-mail address already exists.'

    NAME_ERROR = 'The name should be a string between 3 and 32 characters.'

    EMAIL_ERROR = 'Non valid e-mail address.'

    PASSWORD_ERROR = 'The password should be a string between 8 and 32 characters.'

    PASSWORD_MISMATCH_ERROR = 'The password confirmation should be equal as the password field.'

    ROLE_ERROR = 'The role should be a valid role type.'

    FLAG_UNKNOWN = 'Unknown flag.'

    FLAG_NON_VALID_VALUE = 'Flag value non valid.'

    FLAG_NOT_FOUND = 'Flag not found.'

    ACCOUNT_NOT_FOUND = 'No account found.'

    PASSWORD_CHANGE_NON_VALID = 'Current or new password non valid.'

    PASSWORD_CHANGE_MISMATCH = 'Current password is wrong.'

    PASSWORD_DIFF = 'The new password should be different from the current password.'
