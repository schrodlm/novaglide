from unittest.mock import MagicMock
import pytest
from database.database_query import DBQuery
from configuration_mod import Config
class MockMatch1v1:
    def __init__(self, p1, p2, score):
        self.p1 = p1
        self.p2 = p2
        self.score = score

# Define a mock Player class for testing
class MockPlayer:
    def __init__(self, name, elo):
        self.name = name
        self.elo = elo

# Pytest fixtures for creating DBQuery instances with a mocked connection
@pytest.fixture
def db_query_mocked_connection(monkeypatch):
    config = Config()
    mock_db = DBQuery(config=config.config)  # provide your configuration here
    monkeypatch.setattr(mock_db, 'connection', MagicMock())
    return mock_db

# Pytest fixtures for creating a Match1v1 instance for testing
@pytest.fixture
def mock_match_1v1():
    return MockMatch1v1(MockPlayer("Player1", 1200), MockPlayer("Player2", 1100), (2, 1))

# Pytest fixtures for creating a Match1v1 instance for testing
@pytest.fixture
def mock_player():
    return MockPlayer("User1", 1000)

def test_get_user_games(db_query_mocked_connection, mock_player):
    result = db_query_mocked_connection.get_user_games(mock_player.name)
    assert isinstance(result, tuple)

def test_get_user_won_games(db_query_mocked_connection, mock_player):
    result = db_query_mocked_connection.get_user_won_games(mock_player.name)
    assert isinstance(result, tuple)

def test_get_user_id(db_query_mocked_connection, mock_player):
    result = db_query_mocked_connection.get_user_id(mock_player.name)
    assert isinstance(result, tuple)

def test_get_user_name(db_query_mocked_connection):
    result = db_query_mocked_connection.get_user_name(1)
    assert isinstance(result, tuple)

def test_get_user_elo(db_query_mocked_connection, mock_player):
    result = db_query_mocked_connection.get_user_elo(mock_player.name)
    assert isinstance(result, tuple)

def test_get_user_winrate(db_query_mocked_connection, mock_player):
    result = db_query_mocked_connection.get_user_winrate(mock_player.name)
    assert isinstance(result, tuple)

def test_insert_1v1_game(db_query_mocked_connection, mock_match_1v1):
    db_query_mocked_connection.insert_1v1_game(mock_match_1v1)
