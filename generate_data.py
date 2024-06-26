"""Génere des données aléatoires pour les tables de la base de données."""
from faker import Faker
from sqlalchemy.orm import sessionmaker
from bdd import (get_engine, create_all_tables, get_session, 
                 AddressRef, Airport, Airline, Aircraft, AircraftAirportAirlineFlight,
                 Passenger, PassengerFlightBooking, FlightEvent, TravelRestriction, 
                 FlightEventTL, TravelRestriction, TravelRestrictionTL)
from utilities import (SEAT_NUMBER_PATTERN, FLIGHT_STATUSES, FLIGHT_CLASSES, 
                       AIRCRAFT_TYPE, AIRCRAFT_STATUSES)
import rstr

fake = Faker()

def generate_data(session):
    """Génère des données aléatoires pour les tables de la base de données.
    Les tables remplies sont les suivantes: 
        - address_ref;
        - airports;
        - airlines;
        - aircrafts;
        - aircrafts_airports_airlines_flights;
        - passengers;
        - passengers_flights_bookings;
        - flight_events;
        - tables historiques et tables de traduction."""

    # Étape 1 : Générer des données pour les aéroports et les compagnies aériennes
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

    # Étape 2 : Générer des données pour les avions
    for _ in range(30):
        aircraft = Aircraft(
            manufacturer=fake.company(),
            type=fake.random_element(elements=AIRCRAFT_TYPE),
            places=fake.random_int(min=50, max=500),
            status=fake.random_element(elements=AIRCRAFT_STATUSES),
            creation_date=fake.date_time(),
            created_by=fake.random_int(min=1, max=10),
            last_modification_date=fake.date_time(),
            last_modified_by=fake.random_int(min=1, max=10)
        )
        session.add(aircraft)

    session.commit()

    # Étape 3 : Générer des données pour les vols
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
            status=fake.random_element(elements=FLIGHT_STATUSES),
            creation_date=fake.date_time(),
            created_by=fake.random_int(min=1, max=10),
            last_modification_date=fake.date_time(),
            last_modified_by=fake.random_int(min=1, max=10)
        )
        session.add(flight)

    session.commit()

    # Étape 4 : Générer des données pour les passagers et les réservations
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
            seat_number=rstr.xeger(SEAT_NUMBER_PATTERN),
            class_=fake.random_element(elements=FLIGHT_CLASSES),
            creation_date=fake.date_time(),
            created_by=fake.random_int(min=1, max=10),
            last_modification_date=fake.date_time(),
            last_modified_by=fake.random_int(min=1, max=10)
        )
        session.add(booking)

    session.commit()

    # Étape 5 : Générer des données pour les événements de vol
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

    # Étape 6 : Générer des données pour les restrictions de voyage et leurs traductions
    for _ in range(20):
        restriction = TravelRestriction(
            requirement_id=fake.random_int(min=1, max=100),
            from_country=fake.country(),
            to_country=fake.country(),
            creation_date=fake.date_time(),
            created_by=fake.random_int(min=1, max=10),
            last_modification_date=fake.date_time(),
            last_modified_by=fake.random_int(min=1, max=10)
        )
        session.add(restriction)
        session.commit()  # Commit après l'ajout de la restriction pour obtenir restriction_id

        for lang in ['en', 'fr', 'de', 'es']:
            restriction_tl = TravelRestrictionTL(
                requirement_id=restriction.restriction_id,
                language=lang,
                description=fake.text(max_nb_chars=200),
                creation_date=fake.date_time(),
                created_by=fake.random_int(min=1, max=10),
                last_modification_date=fake.date_time(),
                last_modified_by=fake.random_int(min=1, max=10)
            )
            session.add(restriction_tl)

    session.commit()

    # Étape 7 : Générer des données pour les traductions des événements de vol
    for _ in range(10):
        reason_id = fake.random_int(min=1, max=100)
        for lang in ['en', 'fr', 'de', 'es']:
            event_tl = FlightEventTL(
                reason_id=reason_id,
                language=lang,
                description=fake.text(max_nb_chars=200),
                creation_date=fake.date_time(),
                created_by=fake.random_int(min=1, max=10),
                last_modification_date=fake.date_time(),
                last_modified_by=fake.random_int(min=1, max=10)
            )
            session.add(event_tl)

    session.commit()
