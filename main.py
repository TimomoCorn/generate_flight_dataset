"""Lance le script et génère des données aléatoires pour les tables de la base de données."""
from bdd import get_engine, create_all_tables, get_session
from generate_data import generate_data
from utilities import export_to_csv, to_dict

def main():
    """Fonction principale du script."""
    engine = get_engine()
    create_all_tables(engine)
    session = get_session(engine)
    
    generate_data(session)

    from bdd import (Airport, Airline, Aircraft,
                     AircraftAirportAirlineFlight, Passenger,
                     PassengerFlightBooking, FlightEvent, FlightEventTL, 
                     TravelRestriction, TravelRestrictionTL)
    
    # Export des données au format CSV
    export_to_csv(session, Airport, 'airports')
    export_to_csv(session, Airline, 'airlines')
    export_to_csv(session, Aircraft, 'aircrafts')
    export_to_csv(session, AircraftAirportAirlineFlight, 'flights')
    export_to_csv(session, Passenger, 'passengers')
    export_to_csv(session, PassengerFlightBooking, 'bookings')
    export_to_csv(session, FlightEvent, 'flight_events')
    export_to_csv(session, FlightEventTL, 'flight_events_tl')
    export_to_csv(session, TravelRestriction, 'travel_restrictions')
    export_to_csv(session, TravelRestrictionTL, 'travel_restrictions_tl')

    # Fermeture de la session
    session.commit()
    session.close()

if __name__ == "__main__":
    main()
