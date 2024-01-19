from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_component.environment import Environment
from piracyshield_component.config import Config
from piracyshield_component.security.identifier import Identifier
from piracyshield_component.exception import ApplicationException

from piracyshield_data_storage.cache.storage import CacheStorage

from piracyshield_service.importer.errors import ImporterErrorCode, ImporterErrorMessage

import os

class ImporterSaveFileService(BaseService):

    """
    Reads and writes the content into the cache.
    """

    identifier = None

    data_storage_cache = None

    application_archive_config = None

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self._prepare_configs()

        self._prepare_modules()

    def execute(self, filename: str, content: bytes) -> str | Exception:
        """
        :param filename: the name of the file.
        :param content: the file's content.
        :return: the name of the file with a unique identifier.
        """

        extension = self._get_extension(filename)

        if self._has_supported_extension(extension) == False:
            raise ApplicationException(ImporterErrorCode.EXTENSION_NOT_SUPPORTED, ImporterErrorMessage.EXTENSION_NOT_SUPPORTED)

        # generate a unique name for the file
        unique_filename = self._generate_unique_name(filename)

        try:
            self.data_storage_cache.write(unique_filename, content)

            return unique_filename

        except OSError as e:
            self.logger.error(f'Could not save the file: {e}')

            raise ApplicationException(ImporterErrorCode.GENERIC, ImporterErrorMessage.GENERIC)

    def _generate_identifier(self, filename: str) -> str:
        identifier = self.identifier.generate_short_unsafe()

        return f'{identifier}-{filename}'

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

    def _generate_unique_name(self, filename: str) -> str:
        """
        Attempts to generate a unique name string for the file that will be put in the cache.

        :param filename: the name of the file.
        :return: the newly generated name of the file.
        """

        # TODO: just use a timestamp.

        retries = 5
        current_tries = 0

        while (True):
            # exceeded maximum retries
            if current_tries >= retries:
                raise ApplicationException(ImporterErrorCode.GENERIC, ImporterErrorMessage.GENERIC)

            filename = self._generate_identifier(filename)

            # check if the file already exists
            if not self.data_storage_cache.exists(filename):
                break

            current_tries += 1

        return filename

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        # TODO: should at least validate the name.

        pass

    def _prepare_configs(self) -> None:
        """
        Loads the configs.
        """

        self.application_archive_config = Config('application').get('archive')

    def _prepare_modules(self) -> None:
        """
        Initialize and set the instances.
        """

        self.data_storage_cache = CacheStorage()

        self.identifier = Identifier()
