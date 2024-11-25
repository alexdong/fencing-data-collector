from flask import Flask, render_template, jsonify, request
import csv
from io import StringIO
from models import db, Clubs, Fencers, Bouts, Touches

app = Flask(__name__)

@app.route('/')
def list_bouts():
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
    writer.writerow(['Date', 'Fencer A', 'Fencer B', 'Score A', 'Score B'])
    
    for bout in Bouts.select():
        writer.writerow([
            bout.date.strftime('%Y-%m-%d %H:%M'),
            bout.fencer_a.name,
            bout.fencer_b.name,
            bout.final_score_a,
            bout.final_score_b
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
    return jsonify({'status': 'Timer started'})

@app.route('/api/bout/<int:bout_id>/timer/stop', methods=['POST'])
def stop_timer(bout_id):
    bout = Bouts.get_or_none(Bouts.id == bout_id)
    if bout is None:
        return jsonify({'error': 'Bout not found'}), 404
    return jsonify({'status': 'Timer stopped'})

@app.route('/api/bout/<int:bout_id>/touch', methods=['POST'])
def record_touch(bout_id):
    bout = Bouts.get_or_none(Bouts.id == bout_id)
    if bout is None:
        return jsonify({'error': 'Bout not found'}), 404
        
    required_fields = ['seconds_from_start', 'scorer', 'action_type']
    if not all(field in request.form for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
        
    touch = Touches.create(
        bout=bout,
        seconds_from_start=request.form['seconds_from_start'],
        scorer=request.form['scorer'],
        action_type=request.form['action_type']
    )
    
    return jsonify({'status': 'Touch recorded', 'touch_id': touch.id})

if __name__ == '__main__':
    db.connect()
    app.run(debug=True)
