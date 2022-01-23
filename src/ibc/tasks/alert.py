from ibc.celery import app
from ibc.session import make_request


@app.task
def available_alerts(account_id: str) -> list:
    """Returns Applicant Id with all owner related entities.

    Args:
        account_id (str): The account ID you want a list of alerts for.

    Returns:
        list: A collection of `Alert` resources.
    """
    return make_request(method='get', endpoint=f'/api/iserver/account/{account_id}/alerts')


@app.task
def mta_alerts() -> list:
    """Returns the Mobile Trading Assistant Alert.

    Each login user only has one mobile trading assistant (MTA)
    alert with it's own unique tool id. The tool id cannot be
    changed. When modified a new order Id is generated. MTA alerts
    can not be created or deleted. If you call delete
    /iserver/account/:accountId/alert/:alertId, it will reset MTA
    to default. See here for more information on MTA alerts.

    Returns:
        list: A collection of `MobileTradingAssistantAlert` resource.
    """
    return make_request(method='get', endpoint=f'/api/iserver/account/mta')