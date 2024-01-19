from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.whitelist.model import (
    WhitelistModel,
    WhitelistModelGenreException,
    WhitelistModelFQDNMissingException,
    WhitelistModelFQDNNonValidException,
    WhitelistModelIPv4MissingException,
    WhitelistModelIPv4NonValidException,
    WhitelistModelIPv6MissingException,
    WhitelistModelIPv6NonValidException,
    WhitelistModelRegistrarMissingException,
    WhitelistModelRegistrarNonValidException,
    WhitelistModelASCodeMissingException,
    WhitelistModelASCodeNonValidException
)

from piracyshield_data_storage.whitelist.storage import WhitelistStorage, WhitelistStorageCreateException, WhitelistStorageGetException

from piracyshield_service.whitelist.exists_by_value import WhitelistExistsByValueService

from piracyshield_service.ticket.item.exists_by_value import TicketItemExistsByValueService

from piracyshield_service.whitelist.errors import WhitelistErrorCode, WhitelistErrorMessage

class WhitelistCreateService(BaseService):

    """
    Whitelist creation class.
    """

    ticket_item_exists_by_value_service = None

    whitelist_exists_by_value_service = None

    data_storage = None

    data_model = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(self, genre: str, value: str, created_by: str, registrar: str = None, as_code: str = None) -> bool | Exception:
        model = self._validate_parameters(
            genre = genre,
            value = value,
            is_active = True,
            registrar = registrar,
            as_code = as_code
        )

        # check for duplicates
        if self.whitelist_exists_by_value_service.execute(
            value = model.get('value')
        ):
            raise ApplicationException(WhitelistErrorCode.ITEM_EXISTS, WhitelistErrorMessage.ITEM_EXISTS)

        if self.ticket_item_exists_by_value_service.execute(
            genre = model.get('genre'),
            value = model.get('value')
        ):
            # NOTE: this exposes the information to any user testing a whitelist item value.
            raise ApplicationException(WhitelistErrorCode.ITEM_HAS_TICKET, WhitelistErrorMessage.ITEM_HAS_TICKET)

        document = self._build_document(
            model = model,
            now = Time.now_iso8601(),
            created_by = created_by
        )

        try:
            # insert the data into the database
            self.data_storage.insert(document)

        except WhitelistStorageCreateException as e:
            self.logger.error(f'Error while creating the whitelist item')

            raise ApplicationException(WhitelistErrorCode.GENERIC, WhitelistErrorMessage.GENERIC, e)

        self.logger.info(f'Whitelist item `{document.get("value")}` created by `{document.get("metadata").get("created_by")}`')

        # NOTE: should we consider a task to mark all the pre existent items as whitelisted?

        return True

    def _build_document(self, model: dict, now: str, created_by: str) -> dict:
        document = {
            'genre': model.get('genre'),
            'value': model.get('value'),
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

        match model.get('genre'):
            case 'fqdn':
                document['registrar'] = model.get('registrar')

            case 'ipv4':
                document['as_code'] = model.get('as_code')

            case 'ipv6':
                document['as_code'] = model.get('as_code')

        return document

    def _schedule_task(self):
        pass

    def _validate_parameters(self, genre: str, value: str, is_active: bool, registrar: str = None, as_code: str = None) -> dict:
        try:
            model = self.data_model(
                genre = genre,
                value = value,
                is_active = is_active,
                registrar = registrar,
                as_code = as_code
            )

            return model.to_dict()

        except WhitelistModelGenreException:
            raise ApplicationException(WhitelistErrorCode.NON_VALID_GENRE, WhitelistErrorMessage.NON_VALID_GENRE)

        except WhitelistModelFQDNMissingException:
            raise ApplicationException(WhitelistErrorCode.MISSING_FQDN, WhitelistErrorMessage.MISSING_FQDN)

        except WhitelistModelFQDNNonValidException:
            raise ApplicationException(WhitelistErrorCode.NON_VALID_FQDN, WhitelistErrorMessage.NON_VALID_FQDN)

        except WhitelistModelIPv4MissingException:
            raise ApplicationException(WhitelistErrorCode.MISSING_IPV4, WhitelistErrorMessage.MISSING_IPV4)

        except WhitelistModelIPv4NonValidException:
            raise ApplicationException(WhitelistErrorCode.NON_VALID_IPV4, WhitelistErrorMessage.NON_VALID_IPV4)

        except WhitelistModelIPv6MissingException:
            raise ApplicationException(WhitelistErrorCode.MISSING_IPV6, WhitelistErrorMessage.MISSING_IPV6)

        except WhitelistModelIPv6NonValidException:
            raise ApplicationException(WhitelistErrorCode.NON_VALID_IPV6, WhitelistErrorMessage.NON_VALID_IPV6)

        except WhitelistModelRegistrarMissingException:
            raise ApplicationException(WhitelistErrorCode.MISSING_REGISTRAR, WhitelistErrorMessage.MISSING_REGISTRAR)

        except WhitelistModelRegistrarNonValidException:
            raise ApplicationException(WhitelistErrorCode.NON_VALID_REGISTRAR, WhitelistErrorMessage.NON_VALID_REGISTRAR)

        except WhitelistModelASCodeMissingException:
            raise ApplicationException(WhitelistErrorCode.MISSING_AS_CODE, WhitelistErrorMessage.MISSING_AS_CODE)

        except WhitelistModelASCodeNonValidException:
            raise ApplicationException(WhitelistErrorCode.NON_VALID_AS_CODE, WhitelistErrorMessage.NON_VALID_AS_CODE)

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = WhitelistModel

        self.data_storage = WhitelistStorage()

        self.whitelist_exists_by_value_service = WhitelistExistsByValueService()

        self.ticket_item_exists_by_value_service = TicketItemExistsByValueService()
