from ibc.celery import app
from ibc import make_request


@app.task
def scanners() -> dict:
    """Returns an object contains four lists contain all parameters
    for scanners.

    Returns:
        celery.chain: Task chain returning `Scanner` resources
    """
    return make_request(method='get', endpoint='/api/iserver/scanner/params')


@app.task
def run_scanner(scanner: dict) -> dict:
    """Runs scanner to get a list of contracts.

    Args:
        scanner (dict): A scanner definition that you want to run.

    Returns:
        celery.chain: Task chain returning collection of `contract` resources

    Usage:
        >>> run_scanner(
            scanner={
                "instrument": "STK",
                "type": "NOT_YET_TRADED_TODAY",
                "filter": [
                    {
                        "code": "priceAbove",
                        "value": 50
                    },
                    {
                        "code": "priceBelow",
                        "value": 70
                    },
                    {
                        "code": "volumeAbove",
                        "value": None
                    },
                    {
                        "code": "volumeBelow",
                        "value": None
                    }
                ],
                "location": "STK.US.MAJOR",
                "size": "25"
            }
        )
    """
    return make_request(method='post', endpoint='/api/iserver/scanner/run', json_payload=scanner)
