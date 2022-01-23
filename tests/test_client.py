import unittest

from unittest import TestCase
from configparser import ConfigParser
from src.ibc.client import InteractiveBrokersClient
from src.ibc.tasks.market_data import MarketData
from src.ibc.tasks.accounts import Accounts
from src.ibc.tasks.portfolio_analysis import PortfolioAnalysis
from src.ibc.tasks.customer import Customer
from src.ibc.session import InteractiveBrokersSession
from src.ibc.utils.gateway import ClientPortalGateway
from src.ibc.tasks import PnL
from src.ibc.tasks.contract import Contracts
from src.ibc.tasks.alert import Alerts
from src.ibc.tasks.scanner import Scanners
from src.ibc.tasks import Trades
from src.ibc.tasks import PortfolioAccounts
from src.ibc.tasks.orders import Orders
from src.ibc.tasks.data import Data


class InteractiveBrokersClientTest(TestCase):

    """Will perform a unit test for the `InteractiveBrokersClient` session."""

    def setUp(self) -> None:
        """Set up the InteractiveBroker Client."""

        # Initialize the Parser.
        config = ConfigParser()

        # Read the file.
        config.read('config/config.ini')

        # Get the specified credentials.
        account_number = config.get(
            'interactive_brokers_paper', 'paper_account')
        account_password = config.get(
            'interactive_brokers_paper', 'paper_password')

        # Initialize the client.
        self.ibc_client = InteractiveBrokersClient(
            account_number=account_number,
            password=account_password
        )

    def test_creates_instance_of_client(self):
        """Create an instance and make sure it's a `InteractiveBrokerClient`."""

        self.assertIsInstance(
            self.ibc_client,
            InteractiveBrokersClient
        )

    def test_creates_instance_of_session(self):
        """Create an instance and make sure it's a `InteractiveBrokerSession`."""

        self.assertIsInstance(
            self.ibc_client._session,
            InteractiveBrokersSession
        )

    def test_creates_instance_of_gateway(self):
        """Create an instance and make sure it's a `ClientPortalGateway`."""

        self.assertIsInstance(
            self.ibc_client.client_portal,
            ClientPortalGateway
        )

    def test_creates_instance_of_market_data(self):
        """Create an instance and make sure it's a `MarketData`client."""

        self.assertIsInstance(
            self.ibc_client.market_data,
            MarketData
        )

    def test_creates_instance_of_accounts(self):
        """Create an instance and make sure it's a `Accounts`client."""

        self.assertIsInstance(
            self.ibc_client.accounts,
            Accounts
        )

    def test_creates_instance_of_portfolio_analysis(self):
        """Create an instance and make sure it's a `PortfolioAnalysis`client."""

        self.assertIsInstance(
            self.ibc_client.portfolio_analysis,
            PortfolioAnalysis
        )

    def test_creates_instance_of_customer(self):
        """Create an instance and make sure it's a `Customer`client."""

        self.assertIsInstance(
            self.ibc_client.customers,
            Customer
        )

    def test_creates_instance_of_pnl(self):
        """Create an instance and make sure it's a `PNL`client."""

        self.assertIsInstance(
            self.ibc_client.pnl,
            PnL
        )

    def test_creates_instance_of_contracts(self):
        """Create an instance and make sure it's a `Contracts`client."""

        self.assertIsInstance(
            self.ibc_client.contracts,
            Contracts
        )

    def test_creates_instance_of_alerts(self):
        """Create an instance and make sure it's a `Alerts`client."""

        self.assertIsInstance(
            self.ibc_client.alerts,
            Alerts
        )

    def test_creates_instance_of_scanners(self):
        """Create an instance and make sure it's a `Scanners`client."""

        self.assertIsInstance(
            self.ibc_client.scanners,
            Scanners
        )

    def test_creates_instance_of_trades(self):
        """Create an instance and make sure it's a `Trades`client."""

        self.assertIsInstance(
            self.ibc_client.trades,
            Trades
        )

    def test_creates_instance_of_portfolios(self):
        """Create an instance and make sure it's a `PortfoliosAccounts`client."""

        self.assertIsInstance(
            self.ibc_client.portfolio_accounts,
            PortfolioAccounts
        )

    def test_creates_instance_of_orders(self):
        """Create an instance and make sure it's a `Orders`client."""

        self.assertIsInstance(
            self.ibc_client.orders,
            Orders
        )

    def test_creates_instance_of_data(self):
        """Create an instance and make sure it's a `Data`client."""

        self.assertIsInstance(
            self.ibc_client.data_services,
            Data
        )

    def tearDown(self) -> None:
        """Teardown the `InteractiveBroker` Client."""

        del self.ibc_client


if __name__ == '__main__':
    unittest.main()
