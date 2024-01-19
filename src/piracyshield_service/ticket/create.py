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

from piracyshield_data_model.ticket.status.model import TicketStatusModel

from piracyshield_service.ticket.relation.establish import TicketRelationEstablishService
from piracyshield_service.ticket.relation.abandon import TicketRelationAbandonService

from piracyshield_data_storage.ticket.storage import TicketStorage, TicketStorageCreateException

from piracyshield_service.provider.get_all import ProviderGetAllService
from piracyshield_service.provider.exists_by_identifier import ProviderExistsByIdentifierService

from piracyshield_service.ticket.tasks.ticket_initialize import ticket_initialize_task_caller
from piracyshield_service.ticket.tasks.ticket_autoclose import ticket_autoclose_task_caller

from piracyshield_service.log.ticket.create import LogTicketCreateService

from piracyshield_service.forensic.create_hash import ForensicCreateHashService
from piracyshield_service.forensic.remove_by_ticket import ForensicRemoveByTicketService

from piracyshield_service.dda.is_assigned_to_account import DDAIsAssignedToAccountService

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

from datetime import datetime, timedelta

class TicketCreateService(BaseService):

    """
    Manages the creation of a new ticket.
    """

    dda_is_assigned_to_account_service = None

    forensic_create_hash_service = None

    log_ticket_create_service = None

    ticket_relation_establish_service = None

    ticket_relation_abandon_service = None

    provider_exists_by_identifier_service = None

    provider_get_all_service = None

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
        model = self._validate_parameters(
            ticket_id = self._generate_ticket_id(),
            dda_id = dda_id,
            description = description,
            fqdn = fqdn,
            ipv4 = ipv4,
            ipv6 = ipv6,
            assigned_to = assigned_to
        )

        # check if the DDA identifier is assigned to this account
        if self.dda_is_assigned_to_account_service.execute(
            dda_id = dda_id,
            account_id = created_by
        ) == False:
            raise ApplicationException(TicketErrorCode.UNKNOWN_DDA_IDENTIFIER, TicketErrorMessage.UNKNOWN_DDA_IDENTIFIER)

        # if specified, validate each provider_id
        if assigned_to:
            self._verify_assigned_to(assigned_to)

        # otherwise collect all the providers and assign them to the ticket
        else:
            providers = self.provider_get_all_service.execute()

            model['assigned_to'] = []

            for provider in providers:
                model['assigned_to'].append(provider.get('account_id'))

        self.forensic_create_hash_service.execute(
            ticket_id = model.get('ticket_id'),
            hash_list = forensic_evidence.get('hash'),
            reporter_id = created_by
        )

        # proceed to build the relation item <-> provider
        (fqdn_ticket_items, ipv4_ticket_items, ipv6_ticket_items) = self.ticket_relation_establish_service.execute(
            ticket_id = model.get('ticket_id'),
            providers = model.get('assigned_to'),
            fqdn = model.get('fqdn') or None,
            ipv4 = model.get('ipv4') or None,
            ipv6 = model.get('ipv6') or None
        )

        (initialize_job_id, autoclose_job_id) = self._schedule_task(
            ticket_id = model.get('ticket_id'),
            revoke_time = model.get('settings').get('revoke_time'),
            autoclose_time = model.get('settings').get('autoclose_time')
        )

        document = self._build_document(
            model = model,
            fqdn = fqdn,
            ipv4 = ipv4,
            ipv6 = ipv6,
            now = Time.now_iso8601(),
            created_by = created_by,
            tasks = [   # append the task id so we can cancel its execution if needed
                initialize_job_id,
                autoclose_job_id
            ]
        )

        try:
            # insert the data into the database
            self.data_storage.insert(document)

        except TicketStorageCreateException as e:
            self.ticket_relation_abandon_service.execute(model.get('ticket_id'))

            self.forensic_remove_by_ticket_service.execute(model.get('ticket_id'))

            # clean created tasks
            for single_task in document.get('tasks'):
                self.task_service.remove(single_task)

            self.logger.error(f'Could not create the ticket')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

        # log the operation
        self.log_ticket_create_service.execute(
            ticket_id = model.get('ticket_id'),
            message = f'Initial status set to `{document.get("status")}`.'
        )

        self.logger.info(f'Ticket `{model.get("ticket_id")}` created by `{document.get("metadata").get("created_by")}`')

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

    def _verify_assigned_to(self, assigned_to: list) -> bool | Exception:
        """
        Verifies each provider in the list.

        :param assigned_to: list of valid account identifiers.
        :return: true if correct, exception if not.
        """

        try:
            for provider_id in assigned_to:
                if self.provider_exists_by_identifier_service.execute(
                    account_id = provider_id
                ) == False:
                    raise ApplicationException(TicketErrorCode.NON_EXISTENT_ASSIGNED_TO, TicketErrorMessage.NON_EXISTENT_ASSIGNED_TO)

            return True

        except:
            self.logger.error(f'Could not get assigned accounts: `{assigned_to}`')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

    def _build_document(
        self,
        model: dict,
        fqdn: list,
        ipv4: list,
        ipv6: list,
        tasks: list,
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
            'tasks': tasks,
            'metadata': {
                # creation date
                'created_at': now,

                # same as creation date
                'updated_at': now,

                # who created this ticket
                'created_by': created_by
            }
        }

    def _schedule_task(self, ticket_id: str, revoke_time: int, autoclose_time: int) -> tuple | Exception:
        # schedule the initialization of the ticket
        # move the ticket status to open after X seconds and perform the initial operations
        try:
            initialize_job_id = self.task_service.create(
                task_caller = ticket_initialize_task_caller,
                delay = revoke_time,
                ticket_id = ticket_id
            )

            # move the ticket status to close after X seconds
            autoclose_job_id = self.task_service.create(
                task_caller = ticket_autoclose_task_caller,
                delay = autoclose_time,
                ticket_id = ticket_id
            )

            return (initialize_job_id, autoclose_job_id)

        except Exception as e:
            self.ticket_relation_abandon_service.execute(ticket_id)

            self.forensic_remove_by_ticket_service.execute(ticket_id)

            self.logger.error(f'Could not create the task for `{ticket_id}`')

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

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = TicketModel

        self.data_storage = TicketStorage()

        self.identifier = Identifier()

        self.ticket_relation_establish_service = TicketRelationEstablishService()

        self.ticket_relation_abandon_service = TicketRelationAbandonService()

        self.forensic_create_hash_service = ForensicCreateHashService()

        self.forensic_remove_by_ticket_service = ForensicRemoveByTicketService()

        self.provider_get_all_service = ProviderGetAllService()

        self.provider_exists_by_identifier_service = ProviderExistsByIdentifierService()

        self.log_ticket_create_service = LogTicketCreateService()

        self.dda_is_assigned_to_account_service = DDAIsAssignedToAccountService()
