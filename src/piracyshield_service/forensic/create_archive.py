from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.config import Config
from piracyshield_component.utils.time import Time
from piracyshield_component.exception import ApplicationException

from piracyshield_data_model.forensic.archive.model import ForensicArchiveModel, ForensicArchiveModelNameException

from piracyshield_data_storage.forensic.storage import ForensicStorage, ForensicStorageCreateException, ForensicStorageGetException, ForensicStorageUpdateException

from piracyshield_data_storage.cache.storage import CacheStorage

from piracyshield_service.log.ticket.create import LogTicketCreateService

from piracyshield_service.forensic.tasks.analyze_forensic_archive import analyze_forensic_archive_task_caller

from piracyshield_service.forensic.errors import ForensicErrorCode, ForensicErrorMessage

import os

class ForensicCreateArchiveService(BaseService):

    """
    Manages the upload and schedules the analysis for the evidence archive.
    """

    importer_save_file_service = None

    log_ticket_create_service = None

    data_storage_cache = None

    data_storage = None

    data_model = None

    application_archive_config = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, ticket_id: str, archive_name: str) -> bool | Exception:
        """
        :param ticket_id: the ticket identifier related to the archive.
        :param archive_name: the name of the archive.
        :param archive_content: the data content of the file.
        :return: true if everything is successful.
        """

        model = self._validate_parameters(ticket_id, archive_name)

        # before getting to the expensive operations, let's check if the ticket exists
        if not self._ticket_id_exists(ticket_id):
            raise ApplicationException(ForensicErrorCode.NO_HASH_FOR_TICKET, ForensicErrorMessage.NO_HASH_FOR_TICKET)

        # the file is already in the cache
        if not self.data_storage_cache.exists(archive_name):
            self.logger.debug(f'Forensic evidence `{archive_name}` not found in cache')

            raise ApplicationException(ForensicErrorCode.GENERIC, ForensicErrorMessage.GENERIC)

        extension = self._get_extension(archive_name)

        if self._has_supported_extension(extension) == False:
            raise ApplicationException(ForensicErrorCode.EXTENSION_NOT_SUPPORTED, ForensicErrorMessage.EXTENSION_NOT_SUPPORTED)

        self.logger.debug(f'New forensic evidence `{archive_name}` in cache for ticket `{ticket_id}`')

        try:
            # update ticket with the archive name
            self.data_storage.update_archive_name(
                ticket_id = ticket_id,
                archive_name = archive_name,
                status = model.get('status'),
                updated_at = Time.now_iso8601()
            )

        except ForensicStorageUpdateException as e:
            self.logger.error(f"Could not update the ticket's forensic archive name")

            raise ApplicationException(ForensicErrorCode.GENERIC, ForensicErrorMessage.GENERIC, e)

        self._schedule_task(
            ticket_id = ticket_id
        )

        self.logger.info(f'Scheduled analysis for forensic evidence `{archive_name}` for ticket `{ticket_id}`')

        self.log_ticket_create_service.execute(
            ticket_id = ticket_id,
            message = f'Scheduled analysis for new forensic evidence package `{archive_name}`.'
        )

        return True

    def _ticket_id_exists(self, ticket_id: str) -> bool | Exception:
        """
        Check if the ticket exists.

        :param ticket_id: a ticket identifier.
        :return: true if everything is successful.
        """

        try:
            response = self.data_storage.exists_ticket_id(
                ticket_id = ticket_id
            )

            if response.next():
                self.logger.debug(f'Ticket found for `{ticket_id}`')

                return True

            return False

        except ForensicStorageGetException as e:
            self.logger.error(f'Could not verify `{ticket_id}` existence')

            raise ApplicationException(ForensicErrorCode.GENERIC, ForensicErrorMessage.GENERIC, e)

    def _get_extension(self, filename: str) -> str:
        """
        Extracts the extension from the filename.

        :param filename: the name of the file.
        :return: the extension of the file.
        """

        _, extension = os.path.splitext(filename)

        return extension

    def _has_supported_extension(self, extension: str) -> bool:
        """
        Checks wether the extension is supported.

        :param extension: the extension of the file.
        :return: true if supported.
        """

        return extension.lower() in self.application_archive_config.get('supported_extensions')

    def _schedule_task(self, ticket_id: str) -> bool | Exception:
        """
        Schedules the archive analysis.

        :param ticket_id: a ticket identifier.
        :return: true if everything is successful.
        """

        try:
            # schedule package analysis and upload to storage.
            analysis_task_id = self.task_service.create(
                task_caller = analyze_forensic_archive_task_caller,
                delay = 1,
                ticket_id = ticket_id
            )

            return True

        except Exception as e:
            self.logger.error(f'Could not create the task for `{ticket_id}`')

            raise ApplicationException(ForensicErrorCode.GENERIC, ForensicErrorMessage.GENERIC, e)

    def _validate_parameters(self, ticket_id: str, archive_name: str) -> bool | Exception:
        """
        Validates the inputs.

        :param ticket_id: a ticket identifier.
        :param archive_name: the name of the archive.
        :return: true if everything is successful.
        """

        try:
            model = self.data_model(
                ticket_id = ticket_id,
                name = archive_name
            )

            return model.to_dict()

        except ForensicArchiveModelNameException:
            raise ApplicationException(ForensicErrorCode.ARCHIVE_NAME, ForensicErrorMessage.ARCHIVE_NAME)

    def _prepare_configs(self) -> None:
        """
        Loads the configs.
        """

        self.application_archive_config = Config('application').get('archive')

    def _prepare_modules(self):
        """
        Initialize and set the instances.
        """

        self.data_model = ForensicArchiveModel

        self.data_storage = ForensicStorage()

        self.data_storage_cache = CacheStorage()

        self.log_ticket_create_service = LogTicketCreateService()
