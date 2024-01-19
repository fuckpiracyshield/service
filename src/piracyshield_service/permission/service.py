from __future__ import annotations

from piracyshield_service.base import BaseService

from piracyshield_service.permission.schema import PermissionSchema

from piracyshield_data_model.account.role.model import AccountRoleModel
from piracyshield_data_model.permission.model import PermissionModel

from piracyshield_component.exception import ApplicationException

from piracyshield_service.permission.errors import PermissionErrorCode, PermissionErrorMessage

class PermissionService(BaseService):

    permission_schema = None

    role_model = None

    role = None

    def __init__(self, role: int):
        """
        Inizialize logger and required modules.
        """

        super().__init__()

        self.role = role

        self._prepare_modules()

    def execute(self):
        pass

    def can_create_account(self) -> bool | Exception:
        if self.has_permission(PermissionModel.CREATE_ACCOUNT) == False:
            raise ApplicationException(PermissionErrorCode.ACCOUNT_CREATE_ERROR, PermissionErrorMessage.ACCOUNT_CREATE_ERROR)

        return True

    def can_view_account(self) -> bool | Exception:
        if self.has_permission(PermissionModel.VIEW_ACCOUNT) == False:
            raise ApplicationException(PermissionErrorCode.ACCOUNT_VIEW_ERROR, PermissionErrorMessage.ACCOUNT_VIEW_ERROR)

        return True

    def can_edit_account(self) -> bool | Exception:
        if self.has_permission(PermissionModel.EDIT_ACCOUNT) == False:
            raise ApplicationException(PermissionErrorCode.ACCOUNT_EDIT_ERROR, PermissionErrorMessage.ACCOUNT_EDIT_ERROR)

        return True

    def can_delete_account(self) -> bool | Exception:
        if self.has_permission(PermissionModel.DELETE_ACCOUNT) == False:
            raise ApplicationException(PermissionErrorCode.ACCOUNT_DELETE_ERROR, PermissionErrorMessage.ACCOUNT_DELETE_ERROR)

        return True

    def can_create_ticket(self) -> bool | Exception:
        if self.has_permission(PermissionModel.CREATE_TICKET) == False:
            raise ApplicationException(PermissionErrorCode.TICKET_CREATE_ERROR, PermissionErrorMessage.TICKET_CREATE_ERROR)

        return True

    def can_view_ticket(self) -> bool | Exception:
        if self.has_permission(PermissionModel.VIEW_TICKET) == False:
            raise ApplicationException(PermissionErrorCode.TICKET_VIEW_ERROR, PermissionErrorMessage.TICKET_VIEW_ERROR)

        return True

    def can_edit_ticket(self) -> bool | Exception:
        if self.has_permission(PermissionModel.EDIT_TICKET) == False:
            raise ApplicationException(PermissionErrorCode.TICKET_EDIT_ERROR, PermissionErrorMessage.TICKET_EDIT_ERROR)

        return True

    def can_delete_ticket(self) -> bool | Exception:
        if self.has_permission(PermissionModel.DELETE_TICKET) == False:
            raise ApplicationException(PermissionErrorCode.TICKET_DELETE_ERROR, PermissionErrorMessage.TICKET_DELETE_ERROR)

        return True

    def can_upload_ticket(self) -> bool | Exception:
        if self.has_permission(PermissionModel.UPLOAD_TICKET) == False:
            raise ApplicationException(PermissionErrorCode.TICKET_UPLOAD_ERROR, PermissionErrorMessage.TICKET_UPLOAD_ERROR)

        return True

    def can_create_whitelist_item(self) -> bool | Exception:
        if self.has_permission(PermissionModel.CREATE_WHITELIST_ITEM) == False:
            raise ApplicationException(PermissionErrorCode.WHITELIST_ITEM_CREATE_ERROR, PermissionErrorMessage.WHITELIST_ITEM_CREATE_ERROR)

        return True

    def can_view_whitelist_item(self) -> bool | Exception:
        if self.has_permission(PermissionModel.VIEW_WHITELIST_ITEM) == False:
            raise ApplicationException(PermissionErrorCode.WHITELIST_ITEM_VIEW_ERROR, PermissionErrorMessage.WHITELIST_ITEM_VIEW_ERROR)

        return True

    def can_edit_whitelist_item(self) -> bool | Exception:
        if self.has_permission(PermissionModel.EDIT_WHITELIST_ITEM) == False:
            raise ApplicationException(PermissionErrorCode.WHITELIST_ITEM_EDIT_ERROR, PermissionErrorMessage.WHITELIST_ITEM_EDIT_ERROR)

        return True

    def can_delete_whitelist_item(self) -> bool | Exception:
        if self.has_permission(PermissionModel.DELETE_WHITELIST_ITEM) == False:
            raise ApplicationException(PermissionErrorCode.WHITELIST_ITEM_DELETE_ERROR, PermissionErrorMessage.WHITELIST_ITEM_DELETE_ERROR)

        return True

    def can_create_dda(self) -> bool | Exception:
        if self.has_permission(PermissionModel.CREATE_DDA) == False:
            raise ApplicationException(PermissionErrorCode.DDA_CREATE_ERROR, PermissionErrorMessage.DDA_CREATE_ERROR)

        return True

    def can_view_dda(self) -> bool | Exception:
        if self.has_permission(PermissionModel.VIEW_DDA) == False:
            raise ApplicationException(PermissionErrorCode.DDA_VIEW_ERROR, PermissionErrorMessage.DDA_VIEW_ERROR)

        return True

    def can_edit_dda(self) -> bool | Exception:
        if self.has_permission(PermissionModel.EDIT_DDA) == False:
            raise ApplicationException(PermissionErrorCode.DDA_EDIT_ERROR, PermissionErrorMessage.DDA_EDIT_ERROR)

        return True

    def can_delete_dda(self) -> bool | Exception:
        if self.has_permission(PermissionModel.DELETE_DDA) == False:
            raise ApplicationException(PermissionErrorCode.DDA_DELETE_ERROR, PermissionErrorMessage.DDA_DELETE_ERROR)

        return True

    def has_permission(self, permission: int) -> bool:
        """
        Checks if the permission is available based on the provided role.
        """

        return permission in self.get_permissions(self.role_model)

    def get_permissions(self, role_model: int) -> set:
        """
        Returns the set of permissions associated with the given role model.
        """

        if role_model in self.permission_schema.SCHEMA:
            return self.permission_schema.SCHEMA[role_model]

        else:
            return set()

    def _schedule_task(self):
        pass

    def _validate_parameters(self):
        pass

    def _prepare_configs(self):
        pass

    def _prepare_modules(self):
        self.role_model = AccountRoleModel(self.role)

        self.permission_schema = PermissionSchema()
