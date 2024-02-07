from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.utils.time import Time
from piracyshield_component.security.identifier import Identifier
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.ticket.model import (
    TicketModel,
    TicketModelNoDataException,
    TicketModelTicketIdException,
    TicketModelDDAIdMissingException,
    TicketModelDDAIdNonValidException,
    TicketModelDescriptionException,
    TicketModelFQDNMissingException,
    TicketModelFQDNNonValidException,
    TicketModelIPv4MissingException,
    TicketModelIPv4NonValidException,
    TicketModelIPv6MissingException,
    TicketModelIPv6NonValidException,
    TicketModelAssignedToNonValidException
)

from piracyshield_data_model.ticket.item.model import (
    TicketItemModel,
    TicketItemModelTicketIdentifierNonValidException,
    TicketItemModelTicketItemIdentifierNonValidException,
    TicketItemModelGenreNonValidException,
    TicketItemModelFQDNMissingException,
    TicketItemModelFQDNNonValidException,
    TicketItemModelIPv4MissingException,
    TicketItemModelIPv4NonValidException,
    TicketItemModelIPv6MissingException,
    TicketItemModelIPv6NonValidException,
    TicketItemModelProviderIdentifierMissingException,
    TicketItemModelProviderIdentifierNonValidException
)

from piracyshield_data_storage.ticket.storage import TicketStorage, TicketStorageCreateException

from piracyshield_service.provider.get_active import ProviderGetActiveService
from piracyshield_service.provider.exists_by_identifier import ProviderExistsByIdentifierService

from piracyshield_service.ticket.tasks.ticket_create import ticket_create_task_caller

from piracyshield_service.log.ticket.create import LogTicketCreateService

from piracyshield_service.forensic.create_hash import ForensicCreateHashService
from piracyshield_service.forensic.remove_by_ticket import ForensicRemoveByTicketService

from piracyshield_service.dda.is_assigned_to_account import DDAIsAssignedToAccountService

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage
from piracyshield_service.ticket.item.errors import TicketItemErrorCode, TicketItemErrorMessage

from datetime import datetime, timedelta

class TicketCreateService(BaseService):

    """
    Manages the creation of a new ticket.
    """

    dda_is_assigned_to_account_service = None

    forensic_create_hash_service = None

    log_ticket_create_service = None

    provider_exists_by_identifier_service = None

    provider_get_active_service = None

    ticket_item_data_model = None

    data_model = None

    data_storage = None

    identifier = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_modules()

    def execute(
        self,
        dda_id: str,
        forensic_evidence: list,
        fqdn: list,
        ipv4: list,
        ipv6: list,
        assigned_to: list,
        created_by: str,
        description: str = None
    ) -> tuple | Exception:
        # filter duplicates
        fqdn = list(set(fqdn))
        ipv4 = list(set(ipv4))
        ipv6 = list(set(ipv6))
        assigned_to = list(set(assigned_to))

        # TODO: do not hardcode this.
        # do not procees if ticket items exceed maximum limits
        if len(fqdn) > 1000:
            raise ApplicationException(TicketErrorCode.TOO_MANY_FQDN, TicketErrorMessage.TOO_MANY_FQDN)

        if len(ipv4) > 1000:
            raise ApplicationException(TicketErrorCode.TOO_MANY_IPV4, TicketErrorMessage.TOO_MANY_IPV4)

        if len(ipv6) > 1000:
            raise ApplicationException(TicketErrorCode.TOO_MANY_IPV6, TicketErrorMessage.TOO_MANY_IPV6)

        model = self._validate_parameters(
            ticket_id = self._generate_ticket_id(),
            dda_id = dda_id,
            description = description,
            fqdn = fqdn,
            ipv4 = ipv4,
            ipv6 = ipv6,
            assigned_to = assigned_to
        )

        # formal validation before going on with the creation process
        if fqdn:
            for fqdn_value in fqdn:
                self._validate_ticket_item(
                    ticket_id = model.get('ticket_id'),
                    value = fqdn_value,
                    genre = 'fqdn'
                )

        if ipv4:
            for ipv4_value in ipv4:
                self._validate_ticket_item(
                    ticket_id = model.get('ticket_id'),
                    value = ipv4_value,
                    genre = 'ipv4'
                )

        if ipv6:
            for ipv6_value in ipv6:
                self._validate_ticket_item(
                    ticket_id = model.get('ticket_id'),
                    value = ipv6_value,
                    genre = 'ipv6'
                )

        # verify DDA
        self._verify_dda(
            dda_id = dda_id,
            created_by = created_by
        )

        if len(assigned_to):
            # if specified, validate each provider identifier
            self._verify_assigned_to(assigned_to)

            model['assigned_to'] = assigned_to

        # otherwise collect all the providers and assign them to the ticket
        else:
            model['assigned_to'] = []

            active_providers = self.provider_get_active_service.execute()

            for provider in active_providers:
                provider_id = provider.get('account_id')

                model['assigned_to'].append(provider_id)

        self.forensic_create_hash_service.execute(
            ticket_id = model.get('ticket_id'),
            hash_list = forensic_evidence.get('hash'),
            reporter_id = created_by
        )

        document = self._build_document(
            model = model,
            fqdn = fqdn,
            ipv4 = ipv4,
            ipv6 = ipv6,
            now = Time.now_iso8601(),
            created_by = created_by
        )

        try:
            # insert the data into the database
            self.data_storage.insert(document)

        except TicketStorageCreateException as e:
            self.forensic_remove_by_ticket_service.execute(model.get('ticket_id'))

            self.logger.error(f'Could not create the ticket')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

        # log the operation
        self.log_ticket_create_service.execute(
            ticket_id = model.get('ticket_id'),
            message = f'Initial status set to `{document.get("status")}`.'
        )

        self.logger.info(f'Ticket `{model.get("ticket_id")}` created by `{document.get("metadata").get("created_by")}`')

        # initialize the creation of the ticket items
        self._schedule_task(
            ticket_data = model
        )

        return (
            # ticket identifier
            model.get('ticket_id'),

            # maximium time allowed before the ticket is visible to the providers
            model.get('settings').get('revoke_time')
        )

    def _generate_ticket_id(self) -> str:
        """
        Generates a UUIDv4.
        """

        return self.identifier.generate()

    def _verify_dda(self, dda_id: str, created_by: str) -> bool | Exception:
        # check if the DDA identifier is assigned to this account
        if self.dda_is_assigned_to_account_service.execute(
            dda_id = dda_id,
            account_id = created_by
        ) == False:
            raise ApplicationException(TicketErrorCode.UNKNOWN_DDA_IDENTIFIER, TicketErrorMessage.UNKNOWN_DDA_IDENTIFIER)

        return True

    def _verify_assigned_to(self, assigned_to: list) -> bool | Exception:
        """
        Verifies each provider in the list.

        :param assigned_to: list of valid account identifiers.
        :return: true if correct, exception if not.
        """

        for provider_id in assigned_to:
            if self.provider_exists_by_identifier_service.execute(
                account_id = provider_id
            ) == False:
                self.logger.error(f'Could not get assigned accounts: `{assigned_to}`')

                raise ApplicationException(TicketErrorCode.NON_EXISTENT_ASSIGNED_TO, TicketErrorMessage.NON_EXISTENT_ASSIGNED_TO)

            return True

    def _build_document(
        self,
        model: dict,
        fqdn: list,
        ipv4: list,
        ipv6: list,
        now: str,
        created_by: str
    ):
        return {
            'ticket_id': model.get('ticket_id'),
            'genre': model.get('genre'),
            'dda_id': model.get('dda_id'),
            'description': model.get('description'),
            'fqdn': fqdn,
            'ipv4': ipv4,
            'ipv6': ipv6,
            'status': model.get('status'),
            'assigned_to': model.get('assigned_to'),
            'settings': model.get('settings'),
            'tasks': [],
            'metadata': {
                # creation date
                'created_at': now,

                # same as creation date
                'updated_at': now,

                # who created this ticket
                'created_by': created_by
            }
        }

    def _schedule_task(self, ticket_data: dict) -> None | Exception:
        try:
            self.task_service.create(
                task_caller = ticket_create_task_caller,
                delay = 1,
                ticket_data = ticket_data
            )

        except Exception as e:
            self.logger.error(f'Could not create ticket items for `{ticket_data.get("ticket_id")}`')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _validate_parameters(self, ticket_id: str, dda_id: str, description: str, fqdn: list, ipv4: list, ipv6: list, assigned_to: list) -> dict | Exception:
        try:
            model = self.data_model(
                ticket_id = ticket_id,
                dda_id = dda_id,
                description = description,
                fqdn = fqdn,
                ipv4 = ipv4,
                ipv6 = ipv6,
                assigned_to = assigned_to
            )

            return model.to_dict()

        except TicketModelTicketIdException as e:
            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

        except TicketModelDDAIdMissingException as e:
            raise ApplicationException(TicketErrorCode.MISSING_DDA_IDENTIFIER, TicketErrorMessage.MISSING_DDA_IDENTIFIER)

        except TicketModelDDAIdNonValidException as e:
            raise ApplicationException(TicketErrorCode.NON_VALID_DDA_IDENTIFIER, TicketErrorMessage.NON_VALID_DDA_IDENTIFIER)

        except TicketModelNoDataException:
            raise ApplicationException(TicketErrorCode.NO_DATA, TicketErrorMessage.NO_DATA)

        except TicketModelDescriptionException:
            raise ApplicationException(TicketErrorCode.NON_VALID_DESCRIPTION, TicketErrorMessage.NON_VALID_DESCRIPTION)

        except TicketModelFQDNMissingException:
            raise ApplicationException(TicketErrorCode.MISSING_FQDN, TicketErrorMessage.MISSING_FQDN)

        except TicketModelFQDNNonValidException:
            raise ApplicationException(TicketErrorCode.NON_VALID_FQDN, TicketErrorMessage.NON_VALID_FQDN)

        except TicketModelIPv4MissingException:
            raise ApplicationException(TicketErrorCode.MISSING_IPV4, TicketErrorMessage.MISSING_IPV4)

        except TicketModelIPv4NonValidException:
            raise ApplicationException(TicketErrorCode.NON_VALID_IPV4, TicketErrorMessage.NON_VALID_IPV4)

        except TicketModelIPv6MissingException:
            raise ApplicationException(TicketErrorCode.MISSING_IPV6, TicketErrorMessage.MISSING_IPV6)

        except TicketModelIPv6NonValidException:
            raise ApplicationException(TicketErrorCode.NON_VALID_IPV6, TicketErrorMessage.NON_VALID_IPV6)

        except TicketModelAssignedToNonValidException:
            raise ApplicationException(TicketErrorCode.NON_VALID_ASSIGNED_TO, TicketErrorMessage.NON_VALID_ASSIGNED_TO)

        except TicketModelAssignedToNonValidException:
            raise ApplicationException(TicketErrorCode.NON_VALID_ASSIGNED_TO, TicketErrorMessage.NON_VALID_ASSIGNED_TO)

    def _validate_ticket_item(self, ticket_id: str, value: str, genre: str) -> dict | Exception:
        try:
            self.ticket_item_data_model(
                ticket_id = ticket_id, # placeholder
                ticket_item_id = ticket_id, # placeholder
                provider_id = ticket_id, # placeholder
                value = value,
                genre = genre,
                is_active = False, # placeholder
                is_duplicate = False, # placeholder
                is_whitelisted = False, # placeholder
                is_error = False # placeholder
            )

            return True

        except Exception as e:
            self.logger.error(f'Could not create the ticket item `{value}` for `{ticket_id}`')

            raise ApplicationException(TicketItemErrorCode.GENERIC, TicketItemErrorMessage.GENERIC, e)

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = TicketModel

        self.ticket_item_data_model = TicketItemModel

        self.data_storage = TicketStorage()

        self.identifier = Identifier()

        self.forensic_create_hash_service = ForensicCreateHashService()

        self.forensic_remove_by_ticket_service = ForensicRemoveByTicketService()

        self.provider_get_active_service = ProviderGetActiveService()

        self.provider_exists_by_identifier_service = ProviderExistsByIdentifierService()

        self.log_ticket_create_service = LogTicketCreateService()

        self.dda_is_assigned_to_account_service = DDAIsAssignedToAccountService()
