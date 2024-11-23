from datetime import datetime, timedelta
from typing import List, Dict
import random
from models import (
    db, Clubs, Fencers, Bouts, Touches,
    ACTION_TYPES, FOOTWORK_TYPES, FOOTWORK_COMBOS, BLADE_PREPS,
    BLADE_DIRECTIONS, FEINT_TARGET_CHANGES, TAKING_BLADE_TYPES,
    DISTANCES, HIT_QUALITIES, HIT_TIMINGS, HIT_LINES,
    HIT_TARGETS, PISTE_POSITIONS, PARRY_TYPES, PARRY_NUMBERS,
    PARRY_QUALITIES, EVASION_TYPES, EVASION_TIMINGS,
    EVASION_SUCCESSES, EVASION_FOLLOW_UPS, PRIORITIES,
    OUTCOME_QUALITIES, REFEREE_CALLS, CARDS
)

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
                action_type=random.choice(ACTION_TYPES),
                prep_footwork=random.choice(FOOTWORK_TYPES),
                prep_footwork_combo=random.choice(FOOTWORK_COMBOS),
                prep_blade=random.choice(BLADE_PREPS),
                prep_blade_direction=random.choice(BLADE_DIRECTIONS),
                prep_feint_count=random.randint(0, 3),
                prep_feint_target_changes=random.choice(FEINT_TARGET_CHANGES),
                prep_taking_blade=random.choice(TAKING_BLADE_TYPES),
                distance=random.choice(DISTANCES),
                hit_quality=random.choice(HIT_QUALITIES),
                hit_timing=random.choice(HIT_TIMINGS),
                hit_line=random.choice(HIT_LINES),
                hit_target=random.choice(HIT_TARGETS),
                hit_piste_position=random.choice(PISTE_POSITIONS),
                defense_parry_type=random.choice(PARRY_TYPES),
                defense_parry_number=random.choice(PARRY_NUMBERS),
                defense_parry_quality=random.choice(PARRY_QUALITIES),
                evasion_type=random.choice(EVASION_TYPES),
                evasion_timing=random.choice(EVASION_TIMINGS),
                evasion_success=random.choice(EVASION_SUCCESSES),
                evasion_follow_up=random.choice(EVASION_FOLLOW_UPS),
                outcome_priority=random.choice(PRIORITIES),
                outcome_quality=random.choice(OUTCOME_QUALITIES),
                outcome_referee_call=random.choice(REFEREE_CALLS),
                outcome_card=random.choice(CARDS),
                video_timestamp_start=f"{random.randint(0,59):02d}:{random.randint(0,59):02d}",
                video_timestamp_end=f"{random.randint(0,59):02d}:{random.randint(0,59):02d}",
                video_id=f"video_{random.randint(1000,9999)}",
                notes=f"Point {point+1}"
            )

    print("Test data created successfully!")

if __name__ == '__main__':
    create_test_data(db)
