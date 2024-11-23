from datetime import datetime
from peewee import *

db = SqliteDatabase('fencing.db')

class BaseModel(Model):
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
    action_type = CharField(choices=[
        'attack', 'riposte', 'counter_attack', 'remise', 
        'counter_riposte', 'renewal', 'point_in_line'
    ])

    # Preparation fields
    prep_footwork = CharField(choices=[
        'advance', 'retreat', 'double_advance', 'double_retreat',
        'jump_forward', 'jump_backward', 'fleche', 'none'
    ], default='none')
    prep_footwork_combo = CharField(choices=[
        'advance_lunge', 'retreat_lunge', 'advance_fleche', 'patinando', 'none'
    ], default='none')
    prep_blade = CharField(choices=[
        'engagement', 'beat', 'press', 'absence_of_blade', 'coupe', 'none'
    ], default='none')
    prep_blade_direction = CharField(choices=[
        'direct', 'indirect', 'circular', 'none'
    ], default='none')
    prep_feint_count = IntegerField(default=0)
    prep_feint_target_changes = CharField(choices=[
        'high_low', 'inside_outside', 'same_line', 'none'
    ], default='none')
    prep_taking_blade = CharField(choices=[
        'none', 'bind', 'envelopment', 'croise', 'opposition'
    ], default='none')

    # Distance
    distance = CharField(choices=['close', 'medium', 'long'], default='medium')

    # Hit details
    hit_quality = CharField(choices=[
        'clear', 'flat', 'grazing', 'missed'
    ], default='clear')
    hit_timing = CharField(choices=[
        'immediate', 'delayed', 'stop_hit'
    ], default='immediate')
    hit_line = CharField(choices=[
        'high_outside', 'high_inside', 'low_outside', 'low_inside'
    ], default='high_outside')
    hit_target = CharField(choices=[
        'toe', 'leg', 'hand', 'shoulder', 'chest', 'flank',
        'arm', 'back', 'head', 'thigh'
    ], default='chest')
    hit_piste_position = CharField(choices=[
        'far_left', 'left', 'center', 'right', 'far_right'
    ], default='center')

    # Defense details
    defense_parry_type = CharField(choices=[
        'simple', 'circular', 'counter', 'semi_circular', 'none'
    ], default='none')
    defense_parry_number = CharField(choices=[
        '4', '6', '7', '8', 'prime', 'none'
    ], default='none')
    defense_parry_quality = CharField(choices=[
        'clean', 'beat_parry', 'yielding', 'failed', 'none'
    ], default='none')

    # Body evasion
    evasion_type = CharField(choices=[
        'distance', 'lateral', 'rotational', 'combined', 'none'
    ], default='none')
    evasion_timing = CharField(choices=[
        'before_attack', 'during_attack', 'after_attack', 'none'
    ], default='none')
    evasion_success = CharField(choices=[
        'avoided_hit', 'partial_avoid', 'failed', 'none'
    ], default='none')
    evasion_follow_up = CharField(choices=[
        'return_guard', 'change_distance', 'change_line', 'disengage', 'none'
    ], default='none')

    # Outcome
    outcome_priority = CharField(choices=[
        'attack', 'defense', 'simultaneous', 'none'
    ], default='none')
    outcome_quality = CharField(choices=[
        'clean', 'unclear', 'disputed'
    ], default='clean')
    outcome_referee_call = CharField(choices=[
        'attack_touch', 'defense_touch', 'simultaneous', 'no_touch', 'card'
    ], default='attack_touch')
    outcome_card = CharField(choices=[
        'yellow', 'red', 'black', 'none'
    ], default='none')

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
