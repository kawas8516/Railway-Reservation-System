import uuid
from database_manager import DatabaseManager

class PassengerManager:
    """
    A class to manage passenger operations for the Railway Reservation System.

    This class handles booking, canceling, searching, and displaying passenger tickets,
    as well as checking available seats. It uses DatabaseManager for database interactions.
    """

    MAX_SEATS = 100

    def __init__(self, db_manager=None):
        """
        Initialize the PassengerManager with a DatabaseManager instance.

        Args:
            db_manager (DatabaseManager, optional): The database manager instance. If None, creates a new one.
        """
        self.db_manager = db_manager if db_manager else DatabaseManager()

    def book_ticket(self, name, age):
        """
        Book a ticket for a passenger.

        Generates a unique PNR, checks seat availability, assigns status ('confirmed' or 'waiting'),
        inserts into the database, and returns the PNR and status.

        Args:
            name (str): The passenger's name.
            age (int): The passenger's age.

        Returns:
            tuple: (pnr, status) where pnr is the unique passenger number and status is 'confirmed' or 'waiting'.

        Raises:
            ValueError: If input validation fails.
            Exception: If database operation fails.
        """
        # Input validation
        if not name or not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non-empty string.")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer.")

        # Generate unique PNR
        pnr = str(uuid.uuid4())[:8].upper()  # Simple unique ID

        # Check availability
        confirmed_count = self._get_confirmed_count()
        if confirmed_count < self.MAX_SEATS:
            status = 'confirmed'
        else:
            status = 'waiting'

        # Insert into database
        query = "INSERT INTO passengers (pnr, name, age, status, booking_date) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)"
        params = (pnr, name.strip(), age, status)
        self.db_manager.execute_query(query, params)

        return pnr, status

    def cancel_ticket(self, pnr):
        """
        Cancel a ticket by PNR if it exists and is confirmed.

        Args:
            pnr (str): The passenger number.

        Returns:
            str: Success message.

        Raises:
            ValueError: If PNR does not exist or is not confirmed.
            Exception: If database operation fails.
        """
        # Check if exists and status is confirmed
        passenger = self.search_ticket(pnr)
        if not passenger or passenger['status'] != 'confirmed':
            raise ValueError("Ticket not found or not confirmed.")

        # Delete from database
        query = "DELETE FROM passengers WHERE pnr = %s"
        params = (pnr,)
        self.db_manager.execute_query(query, params)

        # Promote the first waiting passenger to confirmed
        promote_query = """
        UPDATE passengers
        SET status = 'confirmed'
        WHERE pnr = (
            SELECT pnr FROM passengers
            WHERE status = 'waiting'
            ORDER BY booking_date ASC
            LIMIT 1
        )
        """
        self.db_manager.execute_query(promote_query)

        return "Ticket canceled successfully."

    def search_ticket(self, pnr):
        """
        Search for a ticket by PNR.

        Args:
            pnr (str): The passenger number.

        Returns:
            dict or None: Passenger details as a dictionary, or None if not found.
        """
        query = "SELECT pnr, name, age, status FROM passengers WHERE pnr = %s"
        params = (pnr,)
        result = self.db_manager.fetch_one(query, params)
        if result:
            return {'pnr': result[0], 'name': result[1], 'age': result[2], 'status': result[3]}
        return None

    def display_passengers(self):
        """
        Display all passengers.

        Returns:
            list: List of dictionaries containing passenger details.
        """
        query = "SELECT pnr, name, age, status FROM passengers"
        results = self.db_manager.fetch_all(query)
        passengers = []
        for row in results:
            passengers.append({'pnr': row[0], 'name': row[1], 'age': row[2], 'status': row[3]})
        return passengers

    def get_available_seats(self):
        """
        Get the number of available seats.

        Returns:
            int: Number of available seats.
        """
        confirmed_count = self._get_confirmed_count()
        return self.MAX_SEATS - confirmed_count

    def _get_confirmed_count(self):
        """
        Helper method to get the count of confirmed passengers.

        Returns:
            int: Count of confirmed passengers.
        """
        query = "SELECT COUNT(*) FROM passengers WHERE status = 'confirmed'"
        result = self.db_manager.fetch_one(query)
        return result[0] if result else 0