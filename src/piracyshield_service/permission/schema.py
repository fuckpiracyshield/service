from piracyshield_data_model.account.role.model import AccountRoleModel
from piracyshield_data_model.permission.model import PermissionModel

class PermissionSchema:

    SCHEMA = {
        AccountRoleModel.GUEST: {
            PermissionModel.VIEW_TICKET
        },

        AccountRoleModel.INTERNAL: {
            PermissionModel.CREATE_TICKET,
            PermissionModel.VIEW_TICKET,
            PermissionModel.EDIT_TICKET,
            PermissionModel.DELETE_TICKET,
            PermissionModel.UPLOAD_TICKET,
            PermissionModel.CREATE_ACCOUNT,
            PermissionModel.VIEW_ACCOUNT,
            PermissionModel.EDIT_ACCOUNT,
            PermissionModel.DELETE_ACCOUNT,
            PermissionModel.CREATE_WHITELIST_ITEM,
            PermissionModel.VIEW_WHITELIST_ITEM,
            PermissionModel.EDIT_WHITELIST_ITEM,
            PermissionModel.DELETE_WHITELIST_ITEM,
            PermissionModel.CREATE_DDA,
            PermissionModel.VIEW_DDA,
            PermissionModel.EDIT_DDA,
            PermissionModel.DELETE_DDA
        },

        AccountRoleModel.REPORTER: {
            PermissionModel.CREATE_TICKET,
            PermissionModel.VIEW_TICKET,
            PermissionModel.UPLOAD_TICKET,
            PermissionModel.DELETE_TICKET,
            PermissionModel.CREATE_WHITELIST_ITEM,
            PermissionModel.VIEW_WHITELIST_ITEM,
            PermissionModel.EDIT_WHITELIST_ITEM,
            PermissionModel.DELETE_WHITELIST_ITEM,
            # this is required as we need the list of reporter accounts to be assigned to the ticket
            # to allow a future selection of the reporters instead of using all of them.
            PermissionModel.VIEW_ACCOUNT,
            PermissionModel.VIEW_DDA
        },

        AccountRoleModel.PROVIDER: {
            PermissionModel.VIEW_TICKET,
            PermissionModel.EDIT_TICKET,
            PermissionModel.CREATE_WHITELIST_ITEM,
            PermissionModel.VIEW_WHITELIST_ITEM,
            PermissionModel.EDIT_WHITELIST_ITEM,
            PermissionModel.DELETE_WHITELIST_ITEM
        }
    }
