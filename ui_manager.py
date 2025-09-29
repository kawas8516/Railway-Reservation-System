from passenger_manager import PassengerManager

class UIManager:
    """
    A class to manage the user interface for the Railway Reservation System.

    This class handles user authentication, displays the menu, processes user choices,
    and interacts with PassengerManager for reservation operations.
    """

    def __init__(self, passenger_manager):
        """
        Initialize the UIManager with a PassengerManager instance.
        """
        self.passenger_manager = passenger_manager

    def authenticate(self):
        """
        Authenticate the user by prompting for username and password.

        Hardcoded credentials: username 'admin', password 'admin123'.

        Returns:
            bool: True if authentication successful, False otherwise.
        """
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        if username == 'admin' and password == 'admin123':
            print("Authentication successful.")
            return True
        else:
            print("Authentication failed.")
            return False

    def display_menu(self):
        """
        Display the main menu options to the user.
        """
        print("\nRailway Reservation System Menu:")
        print("1. Book Ticket")
        print("2. Cancel Ticket")
        print("3. Search Ticket")
        print("4. Display Passengers")
        print("5. View Available Seats")
        print("6. Exit")

    def run(self):
        """
        Run the main user interface loop.

        First authenticates the user, then displays the menu and handles user choices
        until the user chooses to exit.
        """
        if not self.authenticate():
            return  # Exit if authentication fails

        while True:
            self.display_menu()
            try:
                choice = int(input("Enter your choice (1-6): ").strip())
                if choice == 1:
                    # Book Ticket
                    name = input("Enter passenger name: ").strip()
                    age = int(input("Enter passenger age: ").strip())
                    pnr, status = self.passenger_manager.book_ticket(name, age)
                    print(f"Ticket booked successfully. PNR: {pnr}, Status: {status}")
                elif choice == 2:
                    # Cancel Ticket
                    pnr = input("Enter PNR to cancel: ").strip()
                    message = self.passenger_manager.cancel_ticket(pnr)
                    print(message)
                elif choice == 3:
                    # Search Ticket
                    pnr = input("Enter PNR to search: ").strip()
                    passenger = self.passenger_manager.search_ticket(pnr)
                    if passenger:
                        print(f"PNR: {passenger['pnr']}, Name: {passenger['name']}, Age: {passenger['age']}, Status: {passenger['status']}")
                    else:
                        print("Ticket not found.")
                elif choice == 4:
                    # Display Passengers
                    passengers = self.passenger_manager.display_passengers()
                    if passengers:
                        print("Passengers:")
                        for p in passengers:
                            print(f"PNR: {p['pnr']}, Name: {p['name']}, Age: {p['age']}, Status: {p['status']}")
                    else:
                        print("No passengers found.")
                elif choice == 5:
                    # View Available Seats
                    available = self.passenger_manager.get_available_seats()
                    print(f"Available seats: {available}")
                elif choice == 6:
                    # Exit
                    print("Exiting the system.")
                    break
                else:
                    print("Invalid choice. Please select 1-6.")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")