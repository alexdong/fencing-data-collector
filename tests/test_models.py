import pytest
from peewee import SqliteDatabase
from models import Clubs, Fencers, Bouts, Touches
from tests.test_data import create_test_data, TOP_FENCERS

@pytest.fixture
def test_db():
    """Create a test database and populate it with test data"""
    # Use in-memory SQLite for tests
    test_db = SqliteDatabase(':memory:')
    
    # Bind model classes to test db
    for Model in (Clubs, Fencers, Bouts, Touches):
        Model._meta.database = test_db
        
    create_test_data()
    yield test_db
    test_db.close()

def test_club_creation(test_db):
    """Test that all clubs were created correctly"""
    clubs = {club.name for club in Clubs.select()}
    expected_clubs = {club_name for _, club_name in TOP_FENCERS}
    assert clubs == expected_clubs

def test_fencer_creation(test_db):
    """Test that all fencers were created correctly"""
    fencers = {fencer.name for fencer in Fencers.select()}
    expected_fencers = {fencer_name for fencer_name, _ in TOP_FENCERS}
    assert fencers == expected_fencers

def test_bout_count(test_db):
    """Test that exactly 50 bouts were created"""
    bout_count = Bouts.select().count()
    assert bout_count == 50

def test_bout_scores(test_db):
    """Test that bout scores are valid"""
    for bout in Bouts.select():
        # Winner (A) should have score between 10-15
        assert 10 <= bout.final_score_a <= 15
        # Loser (B) should have lower score than A
        assert bout.final_score_b < bout.final_score_a

def test_touches_per_bout(test_db):
    """Test that touches match final scores"""
    for bout in Bouts.select():
        total_touches = bout.final_score_a + bout.final_score_b
        touch_count = Touches.select().where(Touches.bout == bout).count()
        assert touch_count == total_touches

def test_touch_details(test_db):
    """Test that touch details are valid"""
    for touch in Touches.select():
        # Test required fields
        assert touch.seconds_from_start > 0
        assert touch.scorer in ['A', 'B']
        assert touch.action_type in ['attack', 'riposte', 'counter_attack']
        assert touch.distance in ['close', 'medium', 'long']
        assert touch.hit_quality in ['clear', 'flat', 'grazing']
