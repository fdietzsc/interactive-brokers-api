from typing import Union
from typing import List
from enum import Enum

from celery import chain
from ibc.celery import app
from ibc import make_request


def portfolio_get(account_id: str, endpoint: str, params: dict = None) -> chain:
    return make_request.s(method='get', endpoint='/api/portfolio/accounts') | \
           make_request.si(method='get',
                           endpoint=f'/api/portfolio/{account_id}/{endpoint}',
                           params=params)


def portfolio_post(endpoint: str, account_id: str = None, params: dict = None, json_payload: dict = None) -> chain:
    if account_id is None:
        ep = f'/api/portfolio/{endpoint}'
    else:
        ep = f'/api/portfolio/{account_id}/{endpoint}'

    return make_request.s(method='get', endpoint='/api/portfolio/accounts') | \
           make_request.si(method='post',
                           endpoint=ep,
                           params=params,
                           json_payload=json_payload)


@app.task
def accounts() -> list:
    """Returns the portfolio accounts

    In non-tiered account structures, returns a list of accounts
    for which the user can view position and account information.
    This endpoint must be called prior to calling other /portfolio
    endpoints for those accounts. For querying a list of accounts
    which the user can trade, see /iserver/accounts. For a list
    of subaccounts in tiered account structures (e.g. financial
    advisor or ibroker accounts) see /portfolio/subaccounts.

    Returns:
        list: Task to retrieve portfolio accounts

    """
    return make_request(method='get', endpoint='/api/portfolio/accounts')


@app.task
def sub_accounts() -> list:
    """Returns the portfolio subaccounts

    Used in tiered account structures (such as financial advisor
    and ibroker accounts) to return a list of sub-accounts for
    which the user can view position and account-related information.
    This endpoint must be called prior to calling other /portfolio
    endpoints for those subaccounts. To query a list of accounts
    the user can trade, see /iserver/accounts.

    Returns:
        list: Task to retrieve portfolio subaccounts

    """
    return make_request(method='get', endpoint='/api/portfolio/subaccounts')


@app.task
def account_summary(account_id: str) -> dict:
    """Returns information about margin, cash balances
    and other information related to specified account.

    Args:
        account_id (str): Account for which summary is requested

    Returns:
        dict: Task chain returning the summary
    """
    return portfolio_get(account_id, 'summary')


@app.task
def account_metadata(account_id: str) -> dict:
    """Account information related to account Id.

    /portfolio/accounts or /portfolio/subaccounts
    must be called prior to this endpoint.

    Returns:
        dict: Task chain returning account meta data
    """
    return portfolio_get(account_id, 'meta')


@app.task
def account_ledger(account_id: str) -> dict:
    """Information regarding settled cash, cash balances,
    etc. in the account’s base currency and any other cash
    balances hold in other currencies.

    `/portfolio/accounts` or `/portfolio/subaccounts`
    must be called prior to this endpoint. The list of
    supported currencies is available at:
    https://www.interactivebrokers.com/en/index.php?f=3185

    Returns:
        dict: Task chain returning account ledger info
    """
    return portfolio_get(account_id, 'ledger')


@app.task
def account_allocation(account_id: str) -> dict:
    """Information about the account’s portfolio
    by Asset Class, Industry and Category.

    /portfolio/accounts or /portfolio/subaccounts
    must be called prior to this endpoint. The list of
    supported currencies is available at:
    https://www.interactivebrokers.com/en/index.php?f=3185

    Returns:
        dict: Task chain returning account allocation info
    """
    return portfolio_get(account_id, 'allocation')


@app.task
def portfolio_positions(account_id: str, page_id: int = 0, sort: Union[str, Enum] = None,
                        direction: Union[str, Enum] = None, period: str = None) -> dict:
    """Returns a list of positions for the given account. The endpoint
    supports paging, page’s default size is 30 positions.

    Args:
        account_id (str): The account you want to query for positions.
        page_id (int, optional): The page you want to query. Defaults to 0.
        sort (Union[str, Enum], optional): The field on which to sort the data on. Defaults to None
        direction (Union[str, Enum], optional): The order of the sort, `a` means ascending and `d`
                                               means descending. Defaults to None.
        period (str, optional): The period for pnl column, can be 1D, 7D, 1M... Defaults to None.

    Returns:
        dict: Task chain returning portfolio positions

    Usage:
        >>> res=portfolio_positions.delay('xxxxxxxxx', page_id=0)
        >>> res.get()
    """
    if isinstance(sort, Enum):
        sort = sort.value

    if isinstance(direction, Enum):
        direction = direction.value

    params = {'sort': sort, 'direction': direction, 'period': period }

    return portfolio_get(account_id, f'positions/{page_id}', params=params)


@app.task
def portfolio_allocation(account_ids: List[str]) -> dict:
    """Similar to /portfolio/{accountId}/allocation but
    returns a consolidated view of of all the accounts
    returned by /portfolio/accounts

    /portfolio/accounts or /portfolio/subaccounts
    must be called prior to this endpoint.

    Args:
        account_ids (List[str]): A list of accounts that you want to be consolidated into the view.

    Returns
        dict: Task chain returning consolidated account allocation resources
    """
    return portfolio_post('allocation', json_payload={'acctIds': account_ids})


@app.task
def position_by_contract_id(account_id: str, contract_id: str) -> dict:
    """Returns a list of all positions matching the conid. For portfolio models the
    conid could be in more than one model, returning an array with the name of
    model it belongs to.

    /portfolio/accounts or /portfolio/subaccounts
    must be called prior to this endpoint.

    Args:
        account_id (str): The account you want to query for positions.

        contract_id (str): The contract ID you want to query.

    Returns:
        dict: Task chain returning returning list of positions matching `contract_id`.
    """
    return portfolio_get(account_id, f'/position/{contract_id}')


@app.task
def positions_by_contract_id(contract_id: str ) -> dict:
    """Returns an object of all positions matching the conid for all
    the selected accounts. For portfolio models the conid could be in
    more than one model, returning an array with the name of the model
    it belongs to.

    /portfolio/accounts or /portfolio/subaccounts
    must be called prior to this endpoint.

    Args:
        contract_id (str): The contract ID you want to query.

    Returns:
        dict: Task chain returning returning list of all positions matching `contract_id`.
    """
    return make_request.s(method='get', endpoint='/api/portfolio/accounts') | \
           make_request.si(method='get', endpoint=f'/api/portfolio/positions{contract_id}')


@app.task
def invalidate_positions_cache(account_id: str) -> Union[dict, None]:
    """Invalidates the backend cache of the Portfolio.

    Args:
        account_id (str): The account you want to query for positions.

    Returns:
        Union[dict, None]: Task chain invalidating the backend cache.
    """
    return portfolio_post('/positions/invalidate', account_id=account_id)
