import os
import csv
import re

# Pattern REGEX de notre numéro de siège (exemple: A1, B12, C3, etc.)
SEAT_NUMBER_PATTERN = re.compile(r'^[A-F](?:[1-9]|[1-4][0-9]|50)$')

# Listes de valeurs possibles pour les colonnes de nos tables
FLIGHT_STATUSES = ['Scheduled', 'On time', 'Delayed', 'Diverted', 'Unknown']
FLIGHT_CLASSES = ['Economy', 'Business', 'First']

AIRCRAFT_TYPE = ['Airbus A320', 'Airbus A330', 'Boeing 737', 'Boeing 747', 'Boeing 777', 'Embraer E190']
AIRCRAFT_STATUSES = ['In flight', 'On ground', 'In maintenance', 'In repair', 'On hold']

def to_dict(obj):
    """Convertit un objet SQLAlchemy en dictionnaire Python."""
    return {column.key: getattr(obj, column.key) for column in obj.__table__.columns}

def export_to_csv(session, model_class, filename):
    """Exporte les données d'une table au format CSV."""
    data = session.query(model_class).all()
    dict_data = [to_dict(record) for record in data]

    if dict_data:
        os.makedirs('data', exist_ok=True)

        with open(f'data/{filename}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = dict_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for record in dict_data:
                writer.writerow(record)