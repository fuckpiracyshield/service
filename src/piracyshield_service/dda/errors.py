
class DDAErrorCode:

    GENERIC = '7000'

    MISSING_DESCRIPTION = '7001'

    NON_VALID_DESCRIPTION = '7002'

    MISSING_INSTANCE = '7003'

    NON_VALID_INSTANCE = '7004'

    MISSING_ACCOUNT_ID = '7005'

    NON_VALID_ACCOUNT_ID = '7006'

    NON_VALID_ACCOUNT_ROLE = '7007'

    INSTANCE_EXISTS = '7008'

    CANNOT_REMOVE = '7009'

    INSTANCE_USED = '7010'

    CANNOT_SET_STATUS = '7011'

class DDAErrorMessage:

    GENERIC = 'Error during the creation of the DDA instance.'

    MISSING_DESCRIPTION = 'Missing description.'

    NON_VALID_DESCRIPTION = 'Non valid description.'

    MISSING_INSTANCE = 'Missing instance.'

    NON_VALID_INSTANCE = 'Non valid instance.'

    MISSING_ACCOUNT_ID = 'Missing account identifier.'

    NON_VALID_ACCOUNT_ID = 'Non valid account identifier.'

    NON_VALID_ACCOUNT_ROLE = 'Account with wrong role. Only Reporter accounts are allowed to obtain and use a DDA instance.'

    INSTANCE_EXISTS = 'This item has been already created.'

    CANNOT_REMOVE = 'The item could not be removed. Ensure you have proper permissions or to specify a valid item.'

    INSTANCE_USED = 'A ticket is using this instance, therefore it cannot be removed.'

    CANNOT_SET_STATUS = 'Cannot update the status of the DDA instance.'
