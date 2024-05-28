# main.py
from bdd import get_engine, create_all_tables, get_session
from generate_data import generate_data
import os
import csv

def to_dict(obj):
    return {column.key: getattr(obj, column.key) for column in obj.__table__.columns}

def export_to_csv(session, model_class, filename):
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

def main():
    engine = get_engine()
    create_all_tables(engine)
    session = get_session(engine)
    
    generate_data(session)

    # Export data to CSV
    from bdd import Airport, Airline, Aircraft, AircraftAirportAirlineFlight, Passenger, PassengerFlightBooking, FlightEvent
    
    export_to_csv(session, Airport, 'airports')
    export_to_csv(session, Airline, 'airlines')
    export_to_csv(session, Aircraft, 'aircrafts')
    export_to_csv(session, AircraftAirportAirlineFlight, 'flights')
    export_to_csv(session, Passenger, 'passengers')
    export_to_csv(session, PassengerFlightBooking, 'bookings')
    export_to_csv(session, FlightEvent, 'flight_events')

    # Don't forget to commit any changes and close the session when done
    session.commit()
    session.close()

if __name__ == "__main__":
    main()
