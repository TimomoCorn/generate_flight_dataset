"""Ce document sers à générer des données de test pour une base de données de gestion de vols aériens. 
Les données générées sont ensuite écrites dans des fichiers CSV pour une utilisation ultérieure."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from faker import Faker
import csv

# Constantes utilisées

fly_classes = ['Economy', 'Business', 'First']
aircraft_status = ['Active', 'Inactive', 'Under Maintenance']
flight_status = ['Scheduled', 'Delayed', 'Cancelled', 'On Time']
delay_reasons = ['Weather', 'Technical', 'Operational', 'Security', 'Other']


fake = Faker()

Base = declarative_base()


class Aircraft(Base):
    """Table des avions"""
    __tablename__ = 'aircrafts'

    aircraft_id = Column(Integer, primary_key=True)
    manufacturer = Column(String(100))
    type = Column(String(100))
    places = Column(Integer)
    status = Column(String(50))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class AddressRef(Base):
    """Table des référence d'adresse lié a une table externe à notre base de données"""
    __tablename__ = 'address_ref'

    address_id = Column(Integer, primary_key=True)

class AircraftAirportAirlineFlight(Base):
    """Table des vols d'avion"""
    __tablename__ = 'aircrafts_airports_airlines_flights'

    flight_id = Column(Integer, primary_key=True)
    aircraft_id = Column(Integer, ForeignKey('aircrafts.aircraft_id'))
    departure_airport_id = Column(Integer, ForeignKey('airports.airport_id'))
    arrival_airport_id = Column(Integer, ForeignKey('airports.airport_id'))
    airline_id = Column(Integer, ForeignKey('airlines.airline_id'))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    status = Column(String(50))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class AircraftAirportAirlineFlightH(Base):
    """Table de l'historique des vols d'avion"""
    __tablename__ = 'aircrafts_airports_airlines_flights_H'

    flight_id = Column(Integer, ForeignKey('aircrafts_airports_airlines_flights.flight_id'), primary_key=True)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    status = Column(String(50))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class Airport(Base):
    """Table des aéroports"""
    __tablename__ = 'airports'

    airport_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    address_id = Column(Integer, ForeignKey('address_ref.address_id'))
    iata_code = Column(String(3))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class Airline(Base):
    """Table des compagnies aériennes"""
    __tablename__ = 'airlines'

    airline_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    country = Column(String(100))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class TravelRestriction(Base):
    """Table des restrictions de voyage (COVID-19, voyage dans l'espace Schengen, etc.)"""
    __tablename__ = 'travel_restrictions'

    restriction_id = Column(Integer, primary_key=True)
    requirement_id = Column(Integer, ForeignKey('travel_restrictions_tl.requirement_id'))
    from_country = Column(String(100))
    to_country = Column(String(100))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class TravelRestrictionTL(Base):
    """Table de traduction des restrictions de voyage"""
    __tablename__ = 'travel_restrictions_tl'

    requirement_id = Column(Integer, primary_key=True)
    language = Column(String(50))
    description = Column(String(255))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class Passenger(Base):
    """Table des passagers"""
    __tablename__ = 'passengers'

    passenger_id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(DateTime)
    nationality = Column(String(100))
    address_id = Column(Integer, ForeignKey('address_ref.address_id'))
    passport_number = Column(String(100))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class PassengerFlightBooking(Base):
    """Table des réservations de vols de passagers"""
    __tablename__ = 'passenger_flights_bookings'

    booking_id = Column(Integer, primary_key=True)
    passenger_id = Column(Integer, ForeignKey('passengers.passenger_id'))
    flight_id = Column(Integer, ForeignKey('aircrafts_airports_airlines_flights.flight_id'))
    booking_date = Column(DateTime)
    seat_number = Column(String(10))
    class_ = Column(String(50))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class PassengerFlightBookingH(Base):
    """Table de l'historique des réservations de vols de passagers"""
    __tablename__ = 'passenger_flights_bookings_H'

    booking_id = Column(Integer, ForeignKey('passenger_flights_bookings.booking_id'), primary_key=True)
    booking_date = Column(DateTime)
    class_ = Column(String(50))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class FlightEvent(Base):
    """Table des événements de vol (retards, annulations, etc.)"""
    __tablename__ = 'flights_events'

    event_id = Column(Integer, primary_key=True)
    delay_reason_id = Column(Integer, ForeignKey('flights_events_tl.reason_id'))
    flight_id = Column(Integer, ForeignKey('aircrafts_airports_airlines_flights.flight_id'))
    delay_duration = Column(Integer)
    updated_departure_time = Column(DateTime, nullable=True)
    updated_arrival_time = Column(DateTime, nullable=True)
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class FlightEventH(Base):
    """Table des historiques des événements de vol"""
    __tablename__ = 'flights_events_H'

    event_id = Column(Integer, ForeignKey('flights_events.event_id'), primary_key=True)
    delay_duration = Column(Integer, ForeignKey('flights_events_tl.reason_id'))
    updated_departure_time = Column(DateTime, nullable=True)
    updated_arrival_time = Column(DateTime, nullable=True)
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class FlightEventTL(Base):
    """Table de traduction des événements de vol"""

    __tablename__ = 'flights_events_tl'

    reason_id = Column(Integer, primary_key=True)
    language = Column(String(50))
    description = Column(String(255))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

# Create an engine
engine = create_engine('sqlite:///example.db')  # Example: sqlite database, change as per your database configuration

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Helper function to convert SQLAlchemy objects to dictionaries
def to_dict(obj):
    return {column.key: getattr(obj, column.key) for column in obj.__table__.columns}

# Step 1: Generate data for AddressRef, Airport, and Airline
for _ in range(10):
    address = AddressRef()
    session.add(address)

    airport = Airport(
        name=fake.city() + " Airport",
        address_id=address.address_id,
        iata_code=fake.unique.lexify(text='???'),
        creation_date=fake.date_time(),
        created_by=fake.random_int(min=1, max=10),
        last_modification_date=fake.date_time(),
        last_modified_by=fake.random_int(min=1, max=10)
    )
    session.add(airport)

    airline = Airline(
        name=fake.company(),
        country=fake.country(),
        creation_date=fake.date_time(),
        created_by=fake.random_int(min=1, max=10),
        last_modification_date=fake.date_time(),
        last_modified_by=fake.random_int(min=1, max=10)
    )
    session.add(airline)

session.commit()

# Step 2: Generate data for Aircraft
for _ in range(30):
    aircraft = Aircraft(
        manufacturer=fake.company(),
        type=fake.word(),
        places=fake.random_int(min=50, max=500),
        status=fake.word(),
        creation_date=fake.date_time(start_date='-10y', end_date='now'),
        created_by=fake.random_int(min=1, max=10),
        last_modification_date=fake.date_time(),
        last_modified_by=fake.random_int(min=1, max=10)
    )
    session.add(aircraft)

session.commit()

# Step 3: Generate data for Flights
aircraft_ids = [aircraft.aircraft_id for aircraft in session.query(Aircraft).all()]
airport_ids = [airport.airport_id for airport in session.query(Airport).all()]
airline_ids = [airline.airline_id for airline in session.query(Airline).all()]

for _ in range(50):
    flight = AircraftAirportAirlineFlight(
        aircraft_id=fake.random_element(elements=aircraft_ids),
        departure_airport_id=fake.random_element(elements=airport_ids),
        arrival_airport_id=fake.random_element(elements=airport_ids),
        airline_id=fake.random_element(elements=airline_ids),
        departure_time=fake.date_time(),
        arrival_time=fake.date_time(),
        status=fake.word(),
        creation_date=fake.date_time(),
        created_by=fake.random_int(min=1, max=10),
        last_modification_date=fake.date_time(),
        last_modified_by=fake.random_int(min=1, max=10)
    )
    session.add(flight)

session.commit()

# Step 4: Generate data for Passengers and Bookings
for _ in range(100):
    address = AddressRef()
    session.add(address)

    passenger = Passenger(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        date_of_birth=fake.date_of_birth(),
        nationality=fake.country(),
        address_id=address.address_id,
        passport_number=fake.unique.uuid4(),
        creation_date=fake.date_time(),
        created_by=fake.random_int(min=1, max=10),
        last_modification_date=fake.date_time(),
        last_modified_by=fake.random_int(min=1, max=10)
    )
    session.add(passenger)

session.commit()

passenger_ids = [passenger.passenger_id for passenger in session.query(Passenger).all()]
flight_ids = [flight.flight_id for flight in session.query(AircraftAirportAirlineFlight).all()]

for _ in range(200):
    booking = PassengerFlightBooking(
        passenger_id=fake.random_element(elements=passenger_ids),
        flight_id=fake.random_element(elements=flight_ids),
        booking_date=fake.date_time(),
        seat_number=fake.bothify(text='??###'),
        class_=fake.word(),
        creation_date=fake.date_time(),
        created_by=fake.random_int(min=1, max=10),
        last_modification_date=fake.date_time(),
        last_modified_by=fake.random_int(min=1, max=10)
    )
    session.add(booking)

session.commit()

# Step 5: Generate data for Flight Events
for _ in range(50):
    event = FlightEvent(
        delay_reason_id=fake.random_int(min=1, max=10),
        flight_id=fake.random_element(elements=flight_ids),
        delay_duration=fake.random_int(min=1, max=300),
        updated_departure_time=fake.date_time(),
        updated_arrival_time=fake.date_time(),
        creation_date=fake.date_time(),
        created_by=fake.random_int(min=1, max=10),
        last_modification_date=fake.date_time(),
        last_modified_by=fake.random_int(min=1, max=10)
    )
    session.add(event)

session.commit()

# Query data from the database

airport_data = session.query(Airport).all()
airline_data = session.query(Airline).all()
aircraft_data = session.query(Aircraft).all()
aircraftAirportAirlineFlight_data = session.query(AircraftAirportAirlineFlight).all()
passenger_data = session.query(Passenger).all()
passengerFlightBooking_data = session.query(PassengerFlightBooking).all()
flightEvent_data = session.query(FlightEvent).all()

# Convert query results to dictionaries

airport_data = [to_dict(airport) for airport in airport_data]
airline_data = [to_dict(airline) for airline in airline_data]
aircraft_dicts = [to_dict(aircraft) for aircraft in aircraft_data]
aircraftAirportAirlineFlight_dicts = [to_dict(flight) for flight in aircraftAirportAirlineFlight_data]
passenger_dicts = [to_dict(passenger) for passenger in passenger_data]
passengerFlightBooking_dicts = [to_dict(booking) for booking in passengerFlightBooking_data]
flightEvent_dicts = [to_dict(event) for event in flightEvent_data]

# Write to CSV

def export_to_csv(model_class, filename):
    data = session.query(model_class).all()
    dict_data = [to_dict(record) for record in data]

    if dict_data:
        with open(f'data/{filename}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = dict_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in dict_data:
                writer.writerow(record)

export_to_csv(Airport, 'airports')
export_to_csv(Airline, 'airlines')
export_to_csv(Aircraft, 'aircrafts')
export_to_csv(AircraftAirportAirlineFlight, 'flights')
export_to_csv(Passenger, 'passengers')
export_to_csv(PassengerFlightBooking, 'bookings')
export_to_csv(FlightEvent, 'flight_events')


# Don't forget to commit any changes and close the session when done
session.commit()
session.close()
