from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.security.identifier import Identifier
from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.ticket.error.model import (
    TicketErrorModel,
    TicketErrorModelNoDataException,
    TicketErrorModelTicketErrorIdentifierException,
    TicketErrorModelTicketIdentifierException,
    TicketErrorModelFQDNMissingException,
    TicketErrorModelFQDNNonValidException,
    TicketErrorModelIPv4MissingException,
    TicketErrorModelIPv4NonValidException,
    TicketErrorModelIPv6MissingException,
    TicketErrorModelIPv6NonValidException
)

from piracyshield_data_storage.ticket.error.storage import TicketErrorStorage, TicketErrorStorageCreateException

from piracyshield_service.ticket.get import TicketGetService

from piracyshield_service.ticket.item.get_available_by_ticket import TicketItemGetAvailableByTicketService
from piracyshield_service.ticket.item.set_flag_error import TicketItemSetFlagErrorService

from piracyshield_service.log.ticket.create import LogTicketCreateService

from piracyshield_service.ticket.errors import TicketErrorCode, TicketErrorMessage

class TicketErrorCreateService(BaseService):

    """
    Manages the creation of a new error ticket.
    """

    ticket_item_set_flag_error_service = None

    ticket_get_service = None

    ticket_item_get_available_by_ticket_service = None

    log_ticket_create_service = None

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
        ticket_id: str,
        fqdn: list,
        ipv4: list,
        ipv6: list,
        created_by: str,
    ) -> tuple | Exception:
        model = self._validate_parameters(
            ticket_error_id = self._generate_ticket_error_id(),
            ticket_id = ticket_id,
            fqdn = fqdn,
            ipv4 = ipv4,
            ipv6 = ipv6
        )

        # get ticket if exists
        ticket_data = self.ticket_get_service.execute(
            ticket_id = ticket_id
        )

        # check if the error reporting time has expired
        if Time.is_expired(
            date = ticket_data.get('metadata').get('created_at'),
            expiration_time = ticket_data.get('settings').get('report_error_time')
        ) == True:
            raise ApplicationException(TicketErrorCode.REPORT_ERROR_TIME_EXCEEDED, TicketErrorMessage.REPORT_ERROR_TIME_EXCEEDED)

        # retrieve all the available ticket items
        available_ticket_items = self.ticket_item_get_available_by_ticket_service.execute(
            ticket_id = ticket_id,
            account_id = created_by
        )

        # check if the ticket items are in this ticket and proceed to set the flags
        self._check_and_set_ticket_items(
            ticket_id = ticket_id,
            fqdn_items = fqdn,
            ipv4_items = ipv4,
            ipv6_items = ipv6,
            available_ticket_items = available_ticket_items
        )

        document = self._build_document(
            model = model,
            now = Time.now_iso8601(),
            created_by = created_by
        )

        try:
            # insert the data into the database
            self.data_storage.insert(document)

        except TicketErrorStorageCreateException as e:
            self.logger.error(f'Could not create the error ticket')

            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC, e)

        # log the operation
        self.log_ticket_create_service.execute(
            ticket_id = model.get('ticket_id'),
            message = f'An error ticket has been created with id `{model.get("ticket_error_id")}`.'
        )

        self.logger.info(f'Ticket genre `{model.get("genre")}` with identifier `{model.get("ticket_error_id")}` created by `{document.get("metadata").get("created_by")}`')

        return (
            # error ticket identifier
            model.get('ticket_error_id'),

            # ticket identifier
            model.get('ticket_id')
        )

    def _check_and_set_ticket_items(self,
        ticket_id: str,
        fqdn_items: list,
        ipv4_items: list,
        ipv6_items: list,
        available_ticket_items: list
    ) -> bool | Exception:
        if fqdn_items:
            for fqdn_item in fqdn_items:
                if fqdn_item not in available_ticket_items:
                    raise ApplicationException(TicketErrorCode.NON_VALID_FQDN, TicketErrorMessage.NON_VALID_FQDN)

                else:
                    self.ticket_item_set_flag_error_service.execute(
                        ticket_id = ticket_id,
                        value = fqdn_item,
                        status = True
                    )

        if ipv4_items:
            for ipv4_item in ipv4_items:
                if ipv4_item not in available_ticket_items:
                    raise ApplicationException(TicketErrorCode.NON_VALID_IPV4, TicketErrorMessage.NON_VALID_IPV4)

                else:
                    self.ticket_item_set_flag_error_service.execute(
                        ticket_id = ticket_id,
                        value = ipv4_item,
                        status = True
                    )

        if ipv6_items:
            for ipv6_item in ipv6_items:
                if ipv6_item not in available_ticket_items:
                    raise ApplicationException(TicketErrorCode.NON_VALID_IPV6, TicketErrorMessage.NON_VALID_IPV6)

                else:
                    self.ticket_item_set_flag_error_service.execute(
                        ticket_id = ticket_id,
                        value = ipv6_item,
                        status = True
                    )

        return True

    def _generate_ticket_error_id(self) -> str:
        """
        Generates a UUIDv4.
        """

        return self.identifier.generate()

    def _build_document(self, model: dict, now: str, created_by: str):
        return {
            'ticket_error_id': model.get('ticket_error_id'),
            'genre': model.get('genre'),
            'ticket_id': model.get('ticket_id'),
            'fqdn': model.get('fqdn'),
            'ipv4': model.get('ipv4'),
            'ipv6': model.get('ipv6'),
            'metadata': {
                # creation date
                'created_at': now,

                # who created this ticket
                'created_by': created_by
            }
        }

    def _schedule_task(self):
        pass

    def _validate_parameters(self, ticket_error_id: str, ticket_id: str, fqdn: list, ipv4: list, ipv6: list) -> dict | Exception:
        try:
            model = self.data_model(
                ticket_error_id = ticket_error_id,
                ticket_id = ticket_id,
                fqdn = fqdn,
                ipv4 = ipv4,
                ipv6 = ipv6
            )

            return model.to_dict()

        except TicketErrorModelTicketErrorIdentifierException:
            raise ApplicationException(TicketErrorCode.GENERIC, TicketErrorMessage.GENERIC)

        except TicketErrorModelTicketIdentifierException:
            raise ApplicationException(TicketErrorCode.NON_VALID_TICKET_IDENTIFIER, TicketErrorMessage.NON_VALID_TICKET_IDENTIFIER)

        except TicketErrorModelNoDataException:
            raise ApplicationException(TicketErrorCode.NO_DATA, TicketErrorMessage.NO_DATA)

        except TicketErrorModelFQDNMissingException:
            raise ApplicationException(TicketErrorCode.MISSING_FQDN, TicketErrorMessage.MISSING_FQDN)

        except TicketErrorModelFQDNNonValidException:
            raise ApplicationException(TicketErrorCode.NON_VALID_FQDN, TicketErrorMessage.NON_VALID_FQDN)

        except TicketErrorModelIPv4MissingException:
            raise ApplicationException(TicketErrorCode.MISSING_IPV4, TicketErrorMessage.MISSING_IPV4)

        except TicketErrorModelIPv4NonValidException:
            raise ApplicationException(TicketErrorCode.NON_VALID_IPV4, TicketErrorMessage.NON_VALID_IPV4)

        except TicketErrorModelIPv6MissingException:
            raise ApplicationException(TicketErrorCode.MISSING_IPV6, TicketErrorMessage.MISSING_IPV6)

        except TicketErrorModelIPv6NonValidException:
            raise ApplicationException(TicketErrorCode.NON_VALID_IPV6, TicketErrorMessage.NON_VALID_IPV6)

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.data_model = TicketErrorModel

        self.data_storage = TicketErrorStorage()

        self.identifier = Identifier()

        self.ticket_get_service = TicketGetService()

        self.ticket_item_set_flag_error_service = TicketItemSetFlagErrorService()

        self.ticket_item_get_available_by_ticket_service = TicketItemGetAvailableByTicketService()

        self.log_ticket_create_service = LogTicketCreateService()
