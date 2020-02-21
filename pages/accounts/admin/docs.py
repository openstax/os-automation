"""The Accounts API reference documentation."""

from pages.accounts.admin.base import AccountsAdmin


class APIDocumentation(AccountsAdmin):
    """Accounts API reference documentation."""

    URL_TEMPLATE = '/api/docs/v1'
