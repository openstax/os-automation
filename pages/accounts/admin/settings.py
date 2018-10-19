"""The Accounts security log."""

from pages.accounts.admin.base import AccountsAdmin


class Settings(AccountsAdmin):
    """The Accounts settings page."""

    URL_TEMPLATE = '/settings'
