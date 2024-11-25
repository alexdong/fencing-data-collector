import pytest
from app import app
from models import Clubs, Fencers, Bouts, Touches
from peewee import SqliteDatabase
from tests.test_data import create_test_data

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def test_db():
    """Create a test database and populate it with test data"""
    test_db = SqliteDatabase(':memory:')
    
    # Bind model classes to test db
    for Model in (Clubs, Fencers, Bouts, Touches):
        Model._meta.database = test_db
        
    # Create tables
    test_db.connect()
    test_db.create_tables([Clubs, Fencers, Bouts, Touches])
    
    # Populate test data
    create_test_data(test_db)
    
    yield test_db
    
    test_db.close()

def test_bout_list_page(client, test_db):
    """Test the main bout list page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Fencing Bouts' in response.data
    
    # Check if all bouts are listed
    bout_count = Bouts.select().count()
    assert str(bout_count).encode() in response.data

def test_bout_filter_by_club(client, test_db):
    """Test filtering bouts by club"""
    # Get first club
    club = Clubs.select().first()
    
    response = client.get(f'/api/bouts?club_id={club.id}')
    assert response.status_code == 200
    
    # Check if response contains only bouts from this club
    club_fencer_names = [f.name.encode() for f in club.fencers]
    for name in club_fencer_names:
        assert name in response.data

def test_export_csv(client, test_db):
    """Test CSV export functionality"""
    response = client.get('/api/export-csv')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv'
    assert 'attachment; filename=bouts.csv' in response.headers['Content-Disposition']
    
    # Check CSV content
    csv_lines = response.data.decode().split('\n')
    assert csv_lines[0].startswith('Date,Fencer A,Fencer B,Score,Event')
    assert len(csv_lines) > 1  # Should have header + data

def test_bout_detail_page(client, test_db):
    """Test the bout detail page"""
    # Get first bout
    bout = Bouts.select().first()
    
    response = client.get(f'/bout/{bout.id}')
    assert response.status_code == 200
    
    # Check if bout details are present
    assert bout.fencer_a.name.encode() in response.data
    assert bout.fencer_b.name.encode() in response.data
    assert str(bout.final_score_a).encode() in response.data
    assert str(bout.final_score_b).encode() in response.data

def test_timer_endpoints(client, test_db):
    """Test timer start/stop endpoints"""
    bout = Bouts.select().first()
    
    # Test start timer
    start_response = client.post(f'/api/bout/{bout.id}/timer/start')
    assert start_response.status_code == 200
    assert b'success' in start_response.data
    
    # Test stop timer
    stop_response = client.post(f'/api/bout/{bout.id}/timer/stop')
    assert stop_response.status_code == 200
    assert b'success' in stop_response.data

def test_record_touch(client, test_db):
    """Test recording a new touch"""
    bout = Bouts.select().first()
    
    touch_data = {
        'seconds_from_start': 10,
        'scorer': 'A',
        'action_type': 'counter_attack',
    }
    
    response = client.post(f'/api/bout/{bout.id}/touch', data=touch_data)
    assert response.status_code == 200
    
    # Verify touch was recorded
    touch = Touches.select().where(
        (Touches.bout == bout) & 
        (Touches.seconds_from_start == 10) &
        (Touches.scorer == 'A')
    ).first()
    
    assert touch is not None
    assert touch.action_type == 'attack'

def test_invalid_bout_id(client, test_db):
    """Test accessing invalid bout IDs"""
    invalid_id = 99999
    
    # Test detail page
    detail_response = client.get(f'/bout/{invalid_id}')
    assert detail_response.status_code == 404
    
    # Test touch recording
    touch_response = client.post(f'/api/bout/{invalid_id}/touch')
    assert touch_response.status_code == 404

def test_invalid_touch_data(client, test_db):
    """Test recording touch with invalid data"""
    bout = Bouts.select().first()
    
    # Missing required fields
    response = client.post(f'/api/bout/{bout.id}/touch', data={})
    assert response.status_code == 400
    
    # Invalid action type
    response = client.post(f'/api/bout/{bout.id}/touch', data={
        'scorer': 'A',
        'action_type': 'invalid_action',
        'seconds_from_start': 10
    })
    assert response.status_code == 400
