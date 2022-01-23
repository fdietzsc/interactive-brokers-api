from ibc.celery import app
from ibc.session import make_request


@app.task
def accounts() -> dict:
    """Returns the Users Accounts.

    Returns a list of accounts the user has trading access to,
    their respective aliases and the currently selected account.
    Note this endpoint must be called before modifying an order
    or querying open orders.

    Returns:
        dict: A collection of `Account` resources.

    """
    return make_request(method='get', endpoint='/api/iserver/accounts')


@app.task
def pnl_server_account(self) -> dict:
    """Returns an object containing PnL for the selected account
    and its models (if any).

    Returns:
        dict: An `AccountPnL` resource.
    """
    return make_request(method='get', endpoint='/api/iserver/account/pnl/partitioned')
