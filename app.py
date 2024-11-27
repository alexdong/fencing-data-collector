from flask import Flask, render_template, jsonify, request
import csv
from io import StringIO
from models import db, Clubs, Fencers, Bouts, Touches
from tests.test_data import create_test_data

app = Flask(__name__)

@app.route('/')
def list_bouts():
    # Create test data if no bouts exist
    if Bouts.select().count() == 0:
        create_test_data(db)
    
    clubs = Clubs.select()
    bouts = Bouts.select()
    return render_template('bout_list.html', bouts=bouts, clubs=clubs)

@app.route('/bout/<int:bout_id>')
def bout_detail(bout_id):
    bout = Bouts.get_or_none(Bouts.id == bout_id)
    if bout is None:
        return jsonify({'error': 'Bout not found'}), 404
    return render_template('bout_detail.html', bout=bout)

@app.route('/bout/new')
def new_bout():
    return render_template('bout_form.html')

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad request'}), 400

@app.route('/api/bouts')
def filter_bouts():
    club_id = request.args.get('club_id')
    if club_id:
        bouts = Bouts.select().join(Fencers, on=Bouts.fencer_a).where(Fencers.club_id == club_id)
    else:
        bouts = Bouts.select()
    return render_template('bout_list.html', bouts=bouts)

@app.route('/api/export-csv')
def export_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Fencer A', 'Fencer B', 'Score', 'Event'])
    
    for bout in Bouts.select():
        writer.writerow([
            bout.date.strftime('%Y-%m-%d %H:%M'),
            bout.fencer_a.name,
            bout.fencer_b.name,
            f"{bout.final_score_a}-{bout.final_score_b}",
            bout.event
        ])
    
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=bouts.csv'
    }

@app.route('/api/bout/<int:bout_id>/timer/start', methods=['POST'])
def start_timer(bout_id):
    bout = Bouts.get_or_none(Bouts.id == bout_id)
    if bout is None:
        return jsonify({'error': 'Bout not found'}), 404
    return jsonify({'success': True, 'message': 'Timer started'})

@app.route('/api/bout/<int:bout_id>/timer/stop', methods=['POST'])
def stop_timer(bout_id):
    bout = Bouts.get_or_none(Bouts.id == bout_id)
    if bout is None:
        return jsonify({'error': 'Bout not found'}), 404
    return jsonify({'success': True, 'message': 'Timer stopped'})

@app.route('/api/bout/<int:bout_id>/touch', methods=['POST'])
def record_touch(bout_id):
    bout = Bouts.get_or_none(Bouts.id == bout_id)
    if bout is None:
        return jsonify({'error': 'Bout not found'}), 404
        
    # Get all form data
    data = request.form.to_dict()
    
    # Required fields validation
    required_fields = ['seconds_from_start', 'scorer', 'primary_action']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create touch with all available fields
    touch_data = {
        'bout': bout,
        'seconds_from_start': data['seconds_from_start'],
        'scorer': data['scorer'],
        'action_type': data['primary_action'],
        # Optional fields with defaults
        'prep_footwork': data.get('footwork', 'none'),
        'prep_blade': data.get('blade_preparation', 'none'),
        'distance': data.get('distance', 'medium'),
        'hit_quality': data.get('hit_quality', 'clear'),
        'hit_line': data.get('line', 'high_outside'),
        'hit_target': data.get('specific_target', 'chest'),
        'defense_parry_type': data.get('parry_type', 'none'),
        'defense_parry_number': data.get('parry_number', 'none'),
        'defense_parry_quality': data.get('parry_quality', 'none'),
        'evasion_type': data.get('evasion_type', 'none'),
        'evasion_timing': data.get('evasion_timing', 'none'),
        'evasion_success': data.get('evasion_success', 'none'),
        'evasion_follow_up': data.get('evasion_follow_up', 'none')
    }
    
    touch = Touches.create(**touch_data)
    
    return jsonify({'success': True, 'touch_id': touch.id})

if __name__ == '__main__':
    db.connect()
    app.run(debug=True)
