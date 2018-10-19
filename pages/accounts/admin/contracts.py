"""The Accounts security log."""

from pages.accounts.admin.base import AccountsAdmin


class Contracts(AccountsAdmin):
    """The Accounts legal contracts and policies."""

    URL_TEMPLATE = '/fine_print/contracts'
