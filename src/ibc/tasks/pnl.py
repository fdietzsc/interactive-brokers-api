from ibc.celery import app
from ibc import make_request


@app.task
def pnl_server_account() -> dict:
    """Returns an object containing PnL for the selected account
    and its models (if any).

    Returns:
        dict: An `AccountPnL` resource.
    """
    return make_request(method='get', endpoint='/api/iserver/account/pnl/partitioned')
