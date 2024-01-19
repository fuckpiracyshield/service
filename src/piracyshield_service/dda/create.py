from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.security.identifier import Identifier
from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.dda.model import (
    DDAModel,
    DDAModelDDAIdException,
    DDAModelDescriptionMissingException,
    DDAModelDescriptionNonValidException,
    DDAModelInstanceMissingException,
    DDAModelInstanceNonValidException,
    DDAModelAccountIdMissingException,
    DDAModelAccountIdNonValidException
)

from piracyshield_data_model.account.role.model import AccountRoleModel

from piracyshield_data_storage.dda.storage import DDAStorage, DDAStorageCreateException

from piracyshield_service.account.general.get import GeneralAccountGetService

from piracyshield_service.dda.exists_by_instance import DDAExistsByInstanceService

from piracyshield_service.dda.errors import DDAErrorCode, DDAErrorMessage

class DDACreateService(BaseService):

    """
    DDA creation class.
    """

    general_account_get_service = None

    dda_exists_by_instance_service = None

    identifier = None

    data_storage = None

    data_model = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, description: str, instance: str, account_id: str, created_by: str) -> bool | Exception:
        model = self._validate_parameters(
            dda_id = self._generate_dda_id(),
            description = description,
            instance = instance,
            account_id = account_id,
            is_active = True
        )

        # check for duplicates
        if self.dda_exists_by_instance_service.execute(
            instance = model.get('instance')
        ):
            raise ApplicationException(DDAErrorCode.INSTANCE_EXISTS, DDAErrorMessage.INSTANCE_EXISTS)

        # ensure that the account exists as this will trigger an exception if not
        account_data = self.general_account_get_service.execute(
            account_id = account_id
        )

        # verify it's a reporter account
        if AccountRoleModel.REPORTER.value != account_data.get('role'):
            raise ApplicationException(DDAErrorCode.NON_VALID_ACCOUNT_ROLE, DDAErrorMessage.NON_VALID_ACCOUNT_ROLE)

        document = self._build_document(
            model = model,
            created_by = created_by,
            now = Time.now_iso8601()
        )

        try:
            # insert the data into the database
            self.data_storage.insert(document)

        except DDAStorageCreateException as e:
            self.logger.error(f'Error while creating the DDA instance')

            raise ApplicationException(DDAErrorCode.GENERIC, DDAErrorMessage.GENERIC, e)

        self.logger.info(f'DDA instance `{document.get("instance")}` created by `{document.get("metadata").get("created_by")}`')

        return True

    def _generate_dda_id(self) -> str:
        """
        Generates a UUIDv4.

        :return: a randomly generated 32 characters string.
        """

        return self.identifier.generate()

    def _build_document(self, model: dict, created_by: str, now: str) -> dict:
        return {
            'dda_id': model.get('dda_id'),
            'description': model.get('description'),
            'instance': model.get('instance'),
            'account_id': model.get('account_id'),
            'is_active': model.get('is_active'),
            'metadata': {
                # creation date
                'created_at': now,

                # same as creation date
                'updated_at': now,

                # who created this item
                'created_by': created_by
            }
        }

    def _schedule_task(self):
        pass

    def _validate_parameters(self, dda_id: str, description: str, instance: str, account_id: str, is_active: bool) -> dict | Exception:
        try:
            model = self.data_model(
                dda_id = dda_id,
                description = description,
                instance = instance,
                account_id = account_id,
                is_active = is_active
            )

            return model.to_dict()

        except DDAModelDDAIdException:
            raise ApplicationException(DDAErrorCode.GENERIC, DDAErrorMessage.GENERIC)

        except DDAModelDescriptionMissingException:
            raise ApplicationException(DDAErrorCode.MISSING_DESCRIPTION, DDAErrorMessage.MISSING_DESCRIPTION)

        except DDAModelDescriptionNonValidException:
            raise ApplicationException(DDAErrorCode.NON_VALID_DESCRIPTION, DDAErrorMessage.NON_VALID_DESCRIPTION)

        except DDAModelInstanceMissingException:
            raise ApplicationException(DDAErrorCode.MISSING_INSTANCE, DDAErrorMessage.MISSING_INSTANCE)

        except DDAModelInstanceNonValidException:
            raise ApplicationException(DDAErrorCode.NON_VALID_INSTANCE, DDAErrorMessage.NON_VALID_INSTANCE)

        except DDAModelAccountIdMissingException:
            raise ApplicationException(DDAErrorCode.MISSING_ACCOUNT_ID, DDAErrorMessage.MISSING_ACCOUNT_ID)

        except DDAModelAccountIdNonValidException:
            raise ApplicationException(DDAErrorCode.NON_VALID_ACCOUNT_ID, DDAErrorMessage.NON_VALID_ACCOUNT_ID)

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = DDAModel

        self.data_storage = DDAStorage()

        self.identifier = Identifier()

        self.dda_exists_by_instance_service = DDAExistsByInstanceService()

        self.general_account_get_service = GeneralAccountGetService()
