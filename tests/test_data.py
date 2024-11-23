from datetime import datetime, timedelta
from typing import List, Dict
import random
from models import db, Clubs, Fencers, Bouts, Touches

# Top 10 fencers and their clubs
TOP_FENCERS = [
    ("Alessio Foconi", "Italian Fencing Federation"),
    ("Alexander Massialas", "Massialas Foundation"),
    ("Enzo Lefort", "French Fencing Federation"),
    ("Gerek Meinhardt", "Notre Dame FC"),
    ("Guilherme Toldo", "Brazilian Fencing Federation"),
    ("Ka Long Cheung", "Hong Kong FC"),
    ("Kirill Borodachev", "Russian Fencing Federation"),
    ("Marcus Mepstead", "British Fencing"),
    ("Nick Itkin", "Los Angeles FC"),
    ("Race Imboden", "Brooklyn FC"),
]

def create_test_data(database):
    """Create test data for top 10 fencers and 50 bouts"""

    # Create clubs
    clubs = {}
    for _, club_name in TOP_FENCERS:
        clubs[club_name] = Clubs.create(name=club_name)

    # Create fencers
    fencers = {}
    for fencer_name, club_name in TOP_FENCERS:
        fencers[fencer_name] = Fencers.create(
            name=fencer_name,
            club=clubs[club_name]
        )

    # Create 50 bouts
    base_date = datetime(2024, 1, 1)
    weapons = ['foil', 'epee', 'sabre']
    events = ['World Cup', 'Grand Prix', 'Olympics', 'World Championships']
    
    for i in range(50):
        # Select two random fencers
        fencer_names = random.sample(list(fencers.keys()), 2)
        fencer_a = fencers[fencer_names[0]]
        fencer_b = fencers[fencer_names[1]]
        
        # Random scores (max 15 points)
        score_a = random.randint(10, 15)
        score_b = random.randint(5, score_a-1)  # B always loses
        
        bout = Bouts.create(
            fencer_a=fencer_a,
            fencer_b=fencer_b,
            referee=f"Referee_{random.randint(1,5)}",
            event=random.choice(events),
            weapon=random.choice(weapons),
            date=base_date + timedelta(days=i),
            final_score_a=score_a,
            final_score_b=score_b
        )

        # Create touches for this bout
        for point in range(score_a + score_b):
            seconds = random.randint(1, 180)
            scorer = 'A' if point < score_a else 'B'
            
            Touches.create(
                bout=bout,
                seconds_from_start=seconds,
                scorer=scorer,
                action_type=random.choice(['attack', 'riposte', 'counter_attack', 'remise', 
                                         'counter_riposte', 'renewal', 'point_in_line']),
                prep_footwork=random.choice(['advance', 'retreat', 'double_advance', 'double_retreat',
                                           'jump_forward', 'jump_backward', 'fleche', 'none']),
                prep_footwork_combo=random.choice(['advance_lunge', 'retreat_lunge', 'advance_fleche', 
                                                 'patinando', 'none']),
                prep_blade=random.choice(['engagement', 'beat', 'press', 'absence_of_blade', 
                                        'coupe', 'none']),
                prep_blade_direction=random.choice(['direct', 'indirect', 'circular', 'none']),
                prep_feint_count=random.randint(0, 3),
                prep_feint_target_changes=random.choice(['high_low', 'inside_outside', 'same_line', 'none']),
                prep_taking_blade=random.choice(['none', 'bind', 'envelopment', 'croise', 'opposition']),
                distance=random.choice(['close', 'medium', 'long']),
                hit_quality=random.choice(['clear', 'flat', 'grazing', 'missed']),
                hit_timing=random.choice(['immediate', 'delayed', 'stop_hit']),
                hit_line=random.choice(['high_outside', 'high_inside', 'low_outside', 'low_inside']),
                hit_target=random.choice(['toe', 'leg', 'hand', 'shoulder', 'chest', 'flank',
                                        'arm', 'back', 'head', 'thigh']),
                hit_piste_position=random.choice(['far_left', 'left', 'center', 'right', 'far_right']),
                defense_parry_type=random.choice(['simple', 'circular', 'counter', 'semi_circular', 'none']),
                defense_parry_number=random.choice(['4', '6', '7', '8', 'prime', 'none']),
                defense_parry_quality=random.choice(['clean', 'beat_parry', 'yielding', 'failed', 'none']),
                evasion_type=random.choice(['distance', 'lateral', 'rotational', 'combined', 'none']),
                evasion_timing=random.choice(['before_attack', 'during_attack', 'after_attack', 'none']),
                evasion_success=random.choice(['avoided_hit', 'partial_avoid', 'failed', 'none']),
                evasion_follow_up=random.choice(['return_guard', 'change_distance', 'change_line', 
                                               'disengage', 'none']),
                outcome_priority=random.choice(['attack', 'defense', 'simultaneous', 'none']),
                outcome_quality=random.choice(['clean', 'unclear', 'disputed']),
                outcome_referee_call=random.choice(['attack_touch', 'defense_touch', 'simultaneous', 
                                                  'no_touch', 'card']),
                outcome_card=random.choice(['yellow', 'red', 'black', 'none']),
                video_timestamp_start=f"{random.randint(0,59):02d}:{random.randint(0,59):02d}",
                video_timestamp_end=f"{random.randint(0,59):02d}:{random.randint(0,59):02d}",
                video_id=f"video_{random.randint(1000,9999)}",
                notes=f"Point {point+1}"
            )

    print("Test data created successfully!")

if __name__ == '__main__':
    create_test_data(db)
