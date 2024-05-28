# bdd.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Aircraft(Base):
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
    __tablename__ = 'address_ref'
    address_id = Column(Integer, primary_key=True)

class AircraftAirportAirlineFlight(Base):
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
    __tablename__ = 'airlines'
    airline_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    country = Column(String(100))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class TravelRestriction(Base):
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
    __tablename__ = 'travel_restrictions_tl'
    requirement_id = Column(Integer, primary_key=True)
    language = Column(String(50))
    description = Column(String(255))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class Passenger(Base):
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
    __tablename__ = 'passenger_flights_bookings_H'
    booking_id = Column(Integer, ForeignKey('passenger_flights_bookings.booking_id'), primary_key=True)
    booking_date = Column(DateTime)
    class_ = Column(String(50))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

class FlightEvent(Base):
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
    __tablename__ = 'flights_events_tl'
    reason_id = Column(Integer, primary_key=True)
    language = Column(String(50))
    description = Column(String(255))
    creation_date = Column(DateTime)
    created_by = Column(Integer)
    last_modification_date = Column(DateTime)
    last_modified_by = Column(Integer)

# Create an engine and a sessionmaker
def get_engine():
    return create_engine('sqlite:///example.db')

def create_all_tables(engine):
    Base.metadata.create_all(engine)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
