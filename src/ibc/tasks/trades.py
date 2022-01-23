from ibc.celery import app
from ibc import make_request


@app.task
def get_trades() -> list:
    """Returns a list of trades for the currently selected
    account for current day and six previous days.

    Returns:
        list: A collection of `Trade` resources.
    """
    return make_request(method='get', endpoint='/api/iserver/account/trades')
