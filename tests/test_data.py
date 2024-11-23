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

def create_test_data():
    """Create test data for top 10 fencers and 50 bouts"""
    db.connect()
    db.drop_tables([Touches, Bouts, Fencers, Clubs])
    db.create_tables([Clubs, Fencers, Bouts, Touches])

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
                action_type=random.choice(['attack', 'riposte', 'counter_attack']),
                distance=random.choice(['close', 'medium', 'long']),
                hit_quality=random.choice(['clear', 'flat', 'grazing']),
                hit_line=random.choice(['high_outside', 'high_inside', 'low_outside', 'low_inside']),
                outcome_priority=random.choice(['attack', 'defense', 'simultaneous']),
                notes=f"Point {point+1}"
            )

    print("Test data created successfully!")

if __name__ == '__main__':
    create_test_data()
