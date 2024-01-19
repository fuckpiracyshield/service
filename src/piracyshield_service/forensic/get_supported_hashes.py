from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_data_model.forensic.hash.rule import ForensicHashRule

class ForensicGetSupportedHashesService(BaseService):

    """
    Supported hashes algorithms for the forensic evidence archive.
    """

    def __init__(self):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

    def execute(self) -> list | Exception:
        """
        :return: a list of strings representing the supported hashes.
        """

        return ForensicHashRule().get_hash_types()

    def _validate_parameters(self):
        pass

    def _schedule_task(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        pass
