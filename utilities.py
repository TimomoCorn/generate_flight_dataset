import os
import csv

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
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in dict_data:
                writer.writerow(record)