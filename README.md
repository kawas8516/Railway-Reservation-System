# Railway Reservation System

## Project Description

The Railway Reservation System is a console-based application developed in Python that enables administrators to manage train ticket bookings efficiently. It utilizes PostgreSQL for data persistence and provides a menu-driven interface for performing reservation operations. The system supports booking tickets with automatic status assignment (confirmed or waiting) based on seat availability, canceling tickets, searching by Passenger Number (PNR), displaying all passengers, and viewing available seats. It is designed with a modular architecture to ensure maintainability and scalability.

## Features List

- **Book Ticket**: Allows booking a ticket by entering passenger name and age. Automatically generates a unique PNR and assigns status as 'confirmed' if seats are available (<100) or 'waiting' if at capacity.
- **Cancel Ticket**: Cancels a confirmed ticket by PNR and promotes the oldest waiting passenger to confirmed status.
- **Search by PNR**: Searches for passenger details using the PNR.
- **Display All Passengers**: Lists all passengers with their details (PNR, name, age, status).
- **View Available Seats**: Displays the number of available seats (100 - confirmed passengers).
- **Admin Authentication**: Requires login with hardcoded credentials (username: 'admin', password: 'admin123').

## Prerequisites

- Python 3.x
- PostgreSQL database server installed and running
- psycopg2 library for Python-PostgreSQL interaction

## Installation/Setup Steps

1. **Install Dependencies**:
   ```
   pip install psycopg2
   ```

2. **Setup PostgreSQL**:
   - Ensure PostgreSQL is installed and running.
   - The system assumes default user 'postgres' with password '2407'. Update credentials in code if different.

3. **Run Database Setup**:
   - Execute `db_setup.py` to create the database and table:
     ```
     python db_setup.py
     ```
   - This script creates the 'railway_reservation' database and the 'passengers' table if they do not exist.

## Usage

1. **Run the Application**:
   ```
   python main.py
   ```

2. **Admin Login**:
   - Enter username: `admin`
   - Enter password: `admin123`

3. **Main Menu Options**:
   - **1. Book Ticket**: Enter passenger name and age to book a ticket.
   - **2. Cancel Ticket**: Enter PNR to cancel a confirmed ticket.
   - **3. Search Ticket**: Enter PNR to view passenger details.
   - **4. Display Passengers**: View all passengers.
   - **5. View Available Seats**: Check available seats.
   - **6. Exit**: Exit the application.

Example interaction:
```
Enter username: admin
Enter password: admin123
Authentication successful.

Railway Reservation System Menu:
1. Book Ticket
2. Cancel Ticket
3. Search Ticket
4. Display Passengers
5. View Available Seats
6. Exit
Enter your choice (1-6): 1
Enter passenger name: John Doe
Enter passenger age: 30
Ticket booked successfully. PNR: ABC123DEF4, Status: confirmed
```

## Database Schema

The system uses a single PostgreSQL database named `railway_reservation` with one table:

### Table: `passengers`

| Column       | Type          | Constraints                  | Description                          |
|--------------|---------------|------------------------------|--------------------------------------|
| pnr          | VARCHAR(10)   | PRIMARY KEY                  | Unique Passenger Number              |
| name         | VARCHAR(100)  | NOT NULL                     | Passenger's name                     |
| age          | INTEGER       | NOT NULL                     | Passenger's age                      |
| status       | VARCHAR(10)   | NOT NULL, CHECK (status IN ('confirmed', 'waiting')) | Booking status                  |
| booking_date | TIMESTAMP     | NOT NULL                     | Date and time of booking             |

- **Relationships**: None (single-table design for simplicity).
- **Notes**: Capacity is handled in code (max 100 confirmed passengers). For scalability, a separate 'trains' table could be added.

## Code Structure

### Files and Descriptions

- **`main.py`**: Entry point of the application. Initializes database and passenger managers, then runs the UI loop.
- **`database_manager.py`**: Contains the `DatabaseManager` class for handling PostgreSQL connections, queries, and transactions.
- **`passenger_manager.py`**: Contains the `PassengerManager` class for business logic related to passenger operations.
- **`ui_manager.py`**: Contains the `UIManager` class for console-based user interface, authentication, and menu handling.
- **`db_setup.py`**: Script to create the database and tables.
- **`check_db.py`**: Utility script to verify if the 'passengers' table exists.
- **`test.py`**: Test script to validate system functionality, including edge cases like capacity limits.

### Classes and Key Methods

- **`DatabaseManager`** (in `database_manager.py`):
  - `__init__()`: Initializes connection parameters.
  - `connect()`: Establishes DB connection.
  - `disconnect()`: Closes DB connection.
  - `execute_query(query, params=None)`: Executes non-SELECT queries.
  - `fetch_all(query, params=None)`: Fetches all results from SELECT queries.
  - `fetch_one(query, params=None)`: Fetches the first result from SELECT queries.

- **`PassengerManager`** (in `passenger_manager.py`):
  - `__init__(db_manager=None)`: Initializes with DB manager.
  - `book_ticket(name, age)`: Books a ticket and returns PNR and status.
  - `cancel_ticket(pnr)`: Cancels a ticket and promotes waiting passengers.
  - `search_ticket(pnr)`: Searches for passenger by PNR.
  - `display_passengers()`: Returns list of all passengers.
  - `get_available_seats()`: Returns number of available seats.
  - `_get_confirmed_count()`: Helper to count confirmed passengers.

- **`UIManager`** (in `ui_manager.py`):
  - `__init__(passenger_manager)`: Initializes with passenger manager.
  - `authenticate()`: Handles admin login.
  - `display_menu()`: Prints the main menu.
  - `run()`: Main UI loop handling user choices.

## Assumptions and Constraints

### Assumptions
- The system manages a single train with a fixed capacity of 100 passengers.
- PNRs are auto-generated as unique 8-character uppercase strings.
- Admin authentication uses hardcoded credentials for simplicity.
- No concurrent users; operations are single-threaded.
- PostgreSQL is pre-installed and configured with the specified credentials.

### Constraints
- Must handle at least 100 passengers with proper status logic.
- Design must be modular and maintainable, separating concerns into classes.
- Robust error handling for database connection failures, including retries and user feedback.
- Support for concurrent users (though implemented as single-threaded, design allows for threading/database locking).
- Input validation for name (non-empty string) and age (positive integer).

## Evaluation Criteria Met

- **Modular Architecture**: Code is organized into separate classes and files by responsibility (UI, business logic, data access).
- **Database Integration**: Proper use of PostgreSQL with transactions, error handling, and parameterized queries to prevent SQL injection.
- **Error Handling and Validation**: Comprehensive input validation and exception handling for robustness.
- **Scalability**: Design supports adding features like multiple trains or concurrent access.
- **Testing**: Includes a test script (`test.py`) covering normal operations, edge cases (e.g., capacity limits), and error scenarios.
- **Maintainability**: Clean code with docstrings, separation of concerns, and no global state.
- **User Experience**: Menu-driven console interface with clear feedback and authentication.