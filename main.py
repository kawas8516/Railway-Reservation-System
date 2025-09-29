from database_manager import DatabaseManager
from passenger_manager import PassengerManager
from ui_manager import UIManager

try:
    print("Starting Railway Reservation System...")
    db_manager = DatabaseManager()
    passenger_manager = PassengerManager(db_manager)
    ui_manager = UIManager(passenger_manager)
    ui_manager.run()
except Exception as e:
    print(f"An error occurred: {e}")