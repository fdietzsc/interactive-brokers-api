from ibc.celery import app
from ibc import make_request


@app.task
def customer_info() -> dict:
    """Returns Applicant Id with all owner related entities.

    Returns:
        dict: A customer resource object.
    """
    return make_request(method='get', endpoint='/api/ibcust/entity/info')
