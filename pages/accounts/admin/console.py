"""Accounts admin controls and console."""

from pages.accounts.admin.base import AccountsAdmin


class Console(AccountsAdmin):
    """Accounts admin controls."""

    URL_TEMPLATE = '/console'
