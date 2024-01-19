from __future__ import annotations

from piracyshield_service.account.get_all import AccountGetAllService

from piracyshield_data_storage.reporter.storage import ReporterStorage

class ReporterGetAllService(AccountGetAllService):

    """
    Retrieves all the reporter accounts.
    """

    def __init__(self):
        """
        Pass the data storage to the parent class.
        """

        super().__init__(ReporterStorage)
