from datetime import datetime
from peewee import (
    Model, SqliteDatabase, AutoField, CharField, 
    DateTimeField, ForeignKeyField, IntegerField, TextField
)

# Enum choices
ACTION_TYPES = ['attack', 'riposte', 'counter_attack', 'remise', 
                'counter_riposte', 'renewal', 'point_in_line']

FOOTWORK_TYPES = ['advance', 'retreat', 'double_advance', 'double_retreat',
                  'jump_forward', 'jump_backward', 'fleche', 'none']

FOOTWORK_COMBOS = ['advance_lunge', 'retreat_lunge', 'advance_fleche', 'patinando', 'none']

BLADE_PREPS = ['engagement', 'beat', 'press', 'absence_of_blade', 'coupe', 'none']

BLADE_DIRECTIONS = ['direct', 'indirect', 'circular', 'none']

FEINT_TARGET_CHANGES = ['high_low', 'inside_outside', 'same_line', 'none']

TAKING_BLADE_TYPES = ['none', 'bind', 'envelopment', 'croise', 'opposition']

DISTANCES = ['close', 'medium', 'long']

HIT_QUALITIES = ['clear', 'flat', 'grazing', 'missed']

HIT_TIMINGS = ['immediate', 'delayed', 'stop_hit']

HIT_LINES = ['high_outside', 'high_inside', 'low_outside', 'low_inside']

HIT_TARGETS = ['toe', 'leg', 'hand', 'shoulder', 'chest', 'flank',
               'arm', 'back', 'head', 'thigh']

PISTE_POSITIONS = ['far_left', 'left', 'center', 'right', 'far_right']

PARRY_TYPES = ['simple', 'circular', 'counter', 'semi_circular', 'none']

PARRY_NUMBERS = ['4', '6', '7', '8', 'prime', 'none']

PARRY_QUALITIES = ['clean', 'beat_parry', 'yielding', 'failed', 'none']

EVASION_TYPES = ['distance', 'lateral', 'rotational', 'combined', 'none']

EVASION_TIMINGS = ['before_attack', 'during_attack', 'after_attack', 'none']

EVASION_SUCCESSES = ['avoided_hit', 'partial_avoid', 'failed', 'none']

EVASION_FOLLOW_UPS = ['return_guard', 'change_distance', 'change_line', 'disengage', 'none']

PRIORITIES = ['attack', 'defense', 'simultaneous', 'none']

OUTCOME_QUALITIES = ['clean', 'unclear', 'disputed']

REFEREE_CALLS = ['attack_touch', 'defense_touch', 'simultaneous', 'no_touch', 'card']

CARDS = ['yellow', 'red', 'black', 'none']

db = SqliteDatabase('fencing.db')

class BaseModel(Model):
    """Base model class that sets the database."""
    class Meta:
        database = db


class Clubs(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)
    created_at = DateTimeField(default=datetime.now)

class Fencers(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    club = ForeignKeyField(Clubs, backref='fencers')
    created_at = DateTimeField(default=datetime.now)

class Bouts(BaseModel):
    id = AutoField(primary_key=True)
    fencer_a = ForeignKeyField(Fencers, backref='bouts_as_a')
    fencer_b = ForeignKeyField(Fencers, backref='bouts_as_b')
    referee = CharField()
    event = CharField()
    weapon = CharField()
    date = DateTimeField(default=datetime.now)
    final_score_a = IntegerField(default=0)
    final_score_b = IntegerField(default=0)
    notes = TextField(default='')
    created_at = DateTimeField(default=datetime.now)

class Touches(BaseModel):
    id = AutoField(primary_key=True)
    bout = ForeignKeyField(Bouts, backref='touches')
    seconds_from_start = IntegerField()
    scorer = CharField()  # 'A' or 'B' to indicate which fencer

    # Primary action
    action_type = CharField(choices=ACTION_TYPES)

    # Preparation fields
    prep_footwork = CharField(choices=FOOTWORK_TYPES, default='none')
    prep_footwork_combo = CharField(choices=FOOTWORK_COMBOS, default='none')
    prep_blade = CharField(choices=BLADE_PREPS, default='none')
    prep_blade_direction = CharField(choices=BLADE_DIRECTIONS, default='none')
    prep_feint_count = IntegerField(default=0)
    prep_feint_target_changes = CharField(choices=FEINT_TARGET_CHANGES, default='none')
    prep_taking_blade = CharField(choices=TAKING_BLADE_TYPES, default='none')

    # Distance
    distance = CharField(choices=DISTANCES, default='medium')

    # Hit details
    hit_quality = CharField(choices=HIT_QUALITIES, default='clear')
    hit_timing = CharField(choices=HIT_TIMINGS, default='immediate')
    hit_line = CharField(choices=HIT_LINES, default='high_outside')
    hit_target = CharField(choices=HIT_TARGETS, default='chest')
    hit_piste_position = CharField(choices=PISTE_POSITIONS, default='center')

    # Defense details
    defense_parry_type = CharField(choices=PARRY_TYPES, default='none')
    defense_parry_number = CharField(choices=PARRY_NUMBERS, default='none')
    defense_parry_quality = CharField(choices=PARRY_QUALITIES, default='none')

    # Body evasion
    evasion_type = CharField(choices=EVASION_TYPES, default='none')
    evasion_timing = CharField(choices=EVASION_TIMINGS, default='none')
    evasion_success = CharField(choices=EVASION_SUCCESSES, default='none')
    evasion_follow_up = CharField(choices=EVASION_FOLLOW_UPS, default='none')

    # Outcome
    outcome_priority = CharField(choices=PRIORITIES, default='none')
    outcome_quality = CharField(choices=OUTCOME_QUALITIES, default='clean')
    outcome_referee_call = CharField(choices=REFEREE_CALLS, default='attack_touch')
    outcome_card = CharField(choices=CARDS, default='none')

    # Video reference
    video_timestamp_start = CharField(default='')
    video_timestamp_end = CharField(default='')
    video_id = CharField(default='')

    notes = TextField(default='')
    created_at = DateTimeField(default=datetime.now)

if __name__ == '__main__':
    db.connect()
    db.create_tables([Clubs, Fencers, Bouts, Touches])
    print("Database tables created successfully!")
