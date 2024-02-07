from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.security.identifier import Identifier
from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.forensic.archive.model import ForensicArchiveModel, ForensicArchiveModelNameException
from piracyshield_data_model.forensic.hash.model import ForensicHashModel, ForensicHashModelNotSupportedException, ForensicHashModelStringMissingException, ForensicHashModelNonValidException
from piracyshield_data_model.forensic.hash.rule import ForensicHashRule

from piracyshield_data_storage.forensic.storage import ForensicStorage, ForensicStorageCreateException, ForensicStorageGetException

from piracyshield_service.forensic.errors import ForensicErrorCode, ForensicErrorMessage

class ForensicCreateHashService(BaseService):

    """
    Stores the evidence's hash during the ticket creation.
    """

    data_storage = None

    data_model = None

    identifier = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, ticket_id: str, hash_list: list, reporter_id: str) -> bool | Exception:
        for hash_type, hash_string in hash_list.items():
            model = self._validate_parameters(
                hash_type = hash_type,
                hash_string = hash_string
            )

            document = self._build_document(
                model = model,
                forensic_id = self._generate_forensic_id(),
                ticket_id = ticket_id,
                created_by = reporter_id,
                now = Time.now_iso8601()
            )

            # let's search for a pre-existent hash
            existent_hash = self._hash_string_exists(hash_string)

            # we got one, let's update our new entry with those values
            if existent_hash:
                if 'archive_name' in existent_hash:
                    document['archive_name'] = existent_hash.get('archive_name')

                if 'status' in existent_hash:
                    document['status'] = existent_hash.get('status')

                if 'reason' in existent_hash:
                    document['reason'] = existent_hash.get('reason')

            try:
                self.data_storage.insert(document)

            except ForensicStorageCreateException as e:
                self.logger.error(f"Could not update the ticket's forensic archive hash")

                raise ApplicationException(ForensicErrorCode.GENERIC, ForensicErrorMessage.GENERIC, e)

            self.logger.info(f'Created hash `{hash_string}` for ticket `{ticket_id}`')

        return True

    def _hash_string_exists(self, hash_string: str) -> bool | Exception:
        try:
            response = self.data_storage.exists_hash_string(
                hash_string = hash_string
            )

            if response.empty():
                return False

            self.logger.debug(f'Found pre-existent hash for `{hash_string}`')

            document = next(response, None)

            return document

        except ForensicStorageGetException as e:
            self.logger.error(f'Could not verify `{hash_string}` existence')

            raise ApplicationException(ForensicErrorCode.GENERIC, ForensicErrorMessage.GENERIC, e)

    def _build_document(self, model: dict, forensic_id: str, ticket_id: str, created_by: str, now: str):
        return {
            'forensic_id': forensic_id,
            'ticket_id': ticket_id,
            'hash_type': model.get('hash_type'),
            'hash_string': model.get('hash_string'),
            'metadata': {
                'created_at': now,
                'updated_at': now,
                'created_by': created_by
            }
        }

    def _generate_forensic_id(self) -> str:
        """
        Generates a UUIDv4.

        :return: a randomly generated 32 characters string.
        """

        return self.identifier.generate()

    def _validate_parameters(self, hash_type: str, hash_string: str) -> dict | Exception:
        """
        Validates the inputs.

        :param hash_type: a supported hash algorithm.
        :param hash_string: a valid hash string.
        :return: the data converted into a usable dictionary.
        """

        try:
            model = self.data_model(
                hash_type = hash_type,
                hash_string = hash_string
            )

            return model.to_dict()

        except ForensicHashModelNotSupportedException:
            raise ApplicationException(ForensicErrorCode.HASH_TYPE_NOT_SUPPORTED, ForensicErrorMessage.HASH_TYPE_NOT_SUPPORTED)

        except ForensicHashModelStringMissingException:
            raise ApplicationException(ForensicErrorCode.HASH_STRING_EMPTY, ForensicErrorMessage.HASH_STRING_EMPTY)

        except ForensicHashModelNonValidException:
            raise ApplicationException(ForensicErrorCode.HASH_STRING_NON_VALID, ForensicErrorMessage.HASH_STRING_NON_VALID)

    def _schedule_task(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        """
        Initialize and set the instances.
        """

        self.data_model = ForensicHashModel

        self.data_storage = ForensicStorage()

        self.identifier = Identifier()
