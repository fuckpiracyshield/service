
class AuthenticationErrorCode:

    # NOTE: using duplicate codes to mimic the same issue for the user while keeping track of the exception type internally.

    GENERIC = '2000'

    EMAIL_NON_VALID = '2001'

    EMAIL_NOT_FOUND = '2001'

    USER_NON_ACTIVE = '2001'

    PASSWORD_NON_VALID = '2002'

    PASSWORD_MISMATCH = '2002'

    TOKEN_REFRESH_USER_NON_ACTIVE = '2003'

    TOKEN_MISMATCH = '2003'

    TOKEN_EXPIRED = '2003'

    MAX_LOGIN_ATTEMPTS = '2004'

class AuthenticationErrorMessage:

    GENERIC = 'Generic authentication error.'

    EMAIL_NON_VALID = 'Unable to authenticate, e-mail address format non valid.'

    EMAIL_NOT_FOUND = 'Unable to authenticate.'

    USER_NON_ACTIVE = 'Unable to authenticate.'

    PASSWORD_NON_VALID = 'Unable to authenticate.'

    PASSWORD_MISMATCH = 'Unable to authenticate.'

    TOKEN_REFRESH_EMAIL_NOT_FOUND = 'Unable to refresh the token.'

    TOKEN_REFRESH_USER_NON_ACTIVE = 'Unable to refresh the token.'

    TOKEN_MISMATCH = 'Unable to authenticate, token non valid.'

    TOKEN_EXPIRED = 'Unable to verify the token, expired.'

    MAX_LOGIN_ATTEMPTS = 'Max login attempts reached. Your IP address is temporary banned for {} seconds'
