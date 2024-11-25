from flask import Flask, render_template, jsonify
from models import db, Clubs, Fencers, Bouts, Touches

app = Flask(__name__)

@app.route('/')
def list_bouts():
    bouts = Bouts.select()
    return render_template('bout_list.html', bouts=bouts)

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

if __name__ == '__main__':
    db.connect()
    app.run(debug=True)
