from enum import Enum
import json
import requests
import logging
import urllib3

from typing import Dict
from urllib3.exceptions import InsecureRequestWarning
from fake_useragent import UserAgent
urllib3.disable_warnings(category=InsecureRequestWarning)

from .celery import app


RESOURCE_URL = "https://ibgw:5000/v1"


class Frequency(Enum):
    """Represents the frequency options for the
    `PortfolioAnalysis` service.

    ### Usage
    ----
        >>> from src.enums import Frequency
        >>> Frequency.Daily.value
    """

    Daily = 'D'
    Monthly = 'M'
    Quarterly = 'Q'


class MarketDataFields(Enum):
    """Represents the fields for the
    `MarketDataSnapshot` service.

    ### Usage
    ----
        >>> from src.enums import MarketDataFields
        >>> MarketDataFields.Symbol.value
    """

    LastPrice = '31'
    Symbol = '55'
    Text = '58'
    High = '70'
    Low = '71'
    Position = '72'
    MarketValue = '73'
    AvgPrice = '74'
    UnrealizedPnl = '75'
    FormattedPosition = '76'
    FormattedUnrealizedPnl = '77'
    DailyPnl = '78'
    Change = '82'
    ChangePercent = '83'
    BidPrice = '84'
    AskSize = '85'
    AskPrice = '86'
    Volume = '87'
    BidSize = '88'
    Exchange = '6004'
    Conid = '6008'
    SecType = '6070'
    Months = '6072'
    RegularExpiry = '6073'
    Marker = '6119'
    UnderlyingContract = '6457'
    MarketDataAvailability = '6509'
    CompanyName = '7051'
    AskExch = '7057'
    LastExch = '7058'
    LastSize = '7059'
    BidExch = '7068'
    MarketDataAvailabilityOther = '7084'
    PutCallInterest = '7085'
    PutCallVolume = '7086'
    HistoricVolumePercent = '7087'
    HistoricVolumeClosePercent = '7088'
    OptionVolume = '7089'
    ContractIdAndExchange = '7094'
    ContractDescription = '7219'
    ContractDescriptionOther = '7220'
    ListingExchange = '7221'
    Industry = '7280'
    Category = '7281'
    AverageVolume = '7282'
    OptionImpliedVolatilityPercent = '7283'
    HistoricVolume = '7284'
    PutCallRatio = '7285'
    DividendAmount = '7286'
    DividentYield = '7287'
    Ex = '7288'
    MarketCap = '7289'
    PriceEarningsRatio = '7290'
    EarningsPerShare = '7291'
    CostBasis = '7292'
    FiftyTwoWeekLow = '7293'
    FiftyTwoWeekHigh = '7294'
    Open = '7295'
    Close = '7296'
    Delta = '7308'
    Gamma = '7309'
    Theta = '7310'
    Vega = '7311'
    OptionVolumeChangePercent = '7607'
    ImpliedVolatilityPercent = '7633'
    Mark = '7635'
    ShortableShares = '7636'
    FeeRate = '7637'
    OptionOpenInterest = '7638'
    PercentOfMarketValue = '7639'
    Shortable = '7644'
    MorningstarRating = '7655'
    Dividends = '7671'
    DividendsTtm = '7672'
    EMATwoHundred = '7674'
    EMAOneHundred = '7675'
    EMAFiftyDay = '7676'
    EMATwentyDay = '7677'
    PriceEMATwoHundredDay = '7678'
    PriceEMAOneHundredDay = '7679'
    PriceEMAFiftyDay = '7680'
    PriceEMATwentyDay = '7681'
    ChangeSinceOpen = '7682'
    UpcomingEvent = '7683'
    UpcomingEventDate = '7684'
    UpcomingAnalystMeeting = '7685'
    UpcomingEarnings = '7686'
    UpcomingMiscEvents = '7687'
    RecentAnalystMeeting = '7688'
    RecentEarnings = '7689'
    RecentMiscEvents = '7690'
    ProbabilityOfMaxReturnCustomer = '7694'
    BreakEven = '7695'
    SpxDelta = '7696'
    FuturesOpenInterest = '7697'
    LastYield = '7698'
    BidYield = '7699'
    ProbabilityMaxReturn = '7700'
    ProbabilityMaxLoss = '7702'
    ProfitProbability = '7703'
    OrganizationType = '7704'
    DebtClass = '7705'
    Ratings = '7706'
    BondStateCode = '7707'
    BondType = '7708'
    LastTradingDate = '7714'
    IssueDate = '7715'
    Beta = '7718'
    AskYield = '7720'
    PriorClose = '7741'
    VolumeLong = '7762'
    All = [
        '31', '55', '58', '70', '71', '72', '73', '74', '75', '76', '77', '78', '82', '83', '84', '85', '86', '87', '88', '6004', '6008', '6070', '6072', '6073', '6119', '6457', '6509', '7051', '7057', '7058', '7059', '7068', '7084', '7085', '7086', '7087', '7088', '7089', '7094', '7219', '7220', '7221', '7280', '7281', '7282', '7283', '7284', '7285', '7286', '7287', '7288', '7289', '7290', '7291', '7292', '7293', '7294', '7295',
        '7296', '7308', '7309', '7310', '7311', '7607', '7633', '7635', '7636', '7637', '7638', '7639', '7644', '7655', '7671', '7672', '7674', '7675', '7676', '7677', '7678', '7679', '7680', '7681', '7682', '7683', '7684', '7685', '7686', '7687', '7688', '7689', '7690', '7694', '7695', '7696', '7697', '7698', '7699', '7700', '7702', '7703', '7704', '7705', '7706', '7707', '7708', '7714', '7715', '7718', '7720', '7741', '7762'
    ]


class BarTypes(Enum):
    """Represents the bar types for the
    `MarketDataHistory` service.

    ### Usage
    ----
        >>> from src.enums import BarTypes
        >>> BarTypes.OneMinute.value
    """

    OneMinute = '1min'
    TwoMinute = '2min'
    ThreeMinute = '3min'
    FiveMinute = '5min'
    TenMinute = '10min'
    FifteenMinute = '15min'
    ThirtyMinute = '30min'
    OneHour = '1h'
    TwoHour = '2h'
    ThreeHour = '3h'
    FourHour = '4h'
    EightHour = '8h'
    OneDay = '1d'
    OneWeek = '1w'
    OneMonth = '1m'


class SortDirection(Enum):
    """Represents the sort directions for the
    `PortfolioPositions` service.

    ### Usage
    ----
        >>> from src.enums import SortDirection
        >>> SortDirection.Ascending.value
    """

    Ascending = 'a'
    Descending = 'd'


class SortFields(Enum):
    """Represents the sort fields for the
    `PortfolioPositions` service.

    ### Usage
    ----
        >>> from src.enums import SortFields
        >>> SortFields.MarketPrice.value
    """

    AccountId = 'acctId'
    ContractId = 'conid'
    ContractDescription = 'contractDesc'
    Position = 'position'
    MarketPrice = 'mktPrice'
    MarketValue = 'MktValue'
    Currency = 'USD'
    AverageCost = 'avgCost'
    AveragePrice = 'avgPrice'
    RealizedPnl = 'realizedPnl'
    UnrealizedPnl = 'unrealizedPnl'
    Exchanges = 'exchs'
    ExpirationDate = 'expiry'
    PutOrCall = 'putOrCall'
    Multiplier = 'multiplier'
    Strike = 'strike'
    ExerciseStyle = 'exerciseStyle'
    AssetClass = 'assetClass'
    Model = 'model'
    UnderlyingContractId = 'undConid'
    BaseMarketValue = 'baseMktValue'
    BaseMarketPrice = 'baseMktPrice'
    BaseAverageCost = 'BaseAvgCost'
    BaseAveragePrice = 'BaseAvgPrice'
    BaseRealizedPnl = 'baseRealizedPnl'
    BaseUnrealizedPnl = 'baseUnrealizedPnl'


@app.task
def make_request(method: str, endpoint: str, params: dict = None, json_payload: dict = None) -> Dict:
    """Handles all the requests in the library.

    ### Overview
    ---
    A central function used to handle all the requests made in the library,
    this function handles building the URL, defining Content-Type, passing
    through payloads, and handling any errors that may arise during the
    request.

    ### Parameters
    ----
    method : str
        The Request method, can be one of the following:
        ['get','post','put','delete','patch']

    endpoint : str
        The API URL endpoint, example is 'quotes'

    params : dict (optional, Default={})
        The URL params for the request.

    data : dict (optional, Default={})
    A data payload for a request.

    json_payload : dict (optional, Default={})
        A json data payload for a request

    ### Returns
    ----
    Dict:
        A Dictionary object containing the
        JSON values.
    """

    # Build the URL.
    url = RESOURCE_URL + endpoint
    headers = {"Content-Type": "application/json",
               "User-Agent": UserAgent().ff}

    logging.info(msg="------------------------")
    logging.info(msg=f"JSON Payload: {json_payload}")
    logging.info(msg=f"Request Method: {method}")

    # Make the request.
    if method == 'post':
        response = requests.post(url=url, params=params, json=json_payload, verify=False, headers=headers)
    elif method == 'get':
        response = requests.get(url=url, params=params, json=json_payload, verify=False, headers=headers)
    elif method == 'delete':
        response = requests.delete(url=url, params=params, json=json_payload, verify=False, headers=headers)

    logging.info(msg="URL: {url}".format(url=url))
    logging.info(msg=f'Response Status Code: {response.status_code}')
    logging.info(msg=f'Response Content: {response.text}')

    # If it's okay and no details.
    if response.ok and len(response.content) > 0:

        return response.json()

    elif len(response.content) > 0 and response.ok:

        return {'message': 'response successful',
                'status_code': response.status_code
                }

    elif not response.ok and endpoint =='/api/iserver/account':
        return response.json()

    elif not response.ok:

        if len(response.content) == 0:
            response_data = ''
        else:
            try:
                response_data = response.json()
            except:
                response_data = {'content': response.text}

        # Define the error dict.
        error_dict = {'error_code': response.status_code,
                      'response_url': response.url,
                      'response_body': response_data,
                      'response_request': dict(response.request.headers),
                      'response_method': response.request.method,
                      }

        # Log the error.
        logging.error(msg=json.dumps(obj=error_dict, indent=4))

        raise requests.HTTPError()
