from ibc.celery import app
from ibc import make_request


@app.task
def portfolio_news() -> dict:
    """Returns a news summary for your portfolio.

    Returns:
        list: A collection of `NewsArticle` resources.
    """
    return make_request(method='get', endpoint=f'/api/iserver/news/portfolio')


@app.task
def top_news() -> dict:
    """Returns the top news articles.

    Returns:
        list: A collection of `NewsArticle` resources.
    """
    return make_request(method='get', endpoint=f'/api/iserver/news/top')


@app.task
def news_sources() -> dict:
    """Returns news sources.

    Returns:
        list: A collection of `Sources` resources.
    """
    return make_request(method='get', endpoint=f'/api/iserver/news/top')


@app.task
def news_briefings() -> dict:
    """Returns news briefings.

    Returns:
        list: A collection of `Briefings` resources.
    """
    return make_request(method='get', endpoint=f'/api/iserver/news/briefing')


@app.task
def summary(contract_id: str) -> dict:
    """Returns a summary of the contract ID, items include
    company description and more.

    Args:
        contract_id (str): The contract Id you want to query.

    Returns:
        list: A collection of `Summary` resources.
    """
    return make_request(method='get', endpoint=f'/api/iserver/fundamentals/{contract_id}/summary')
