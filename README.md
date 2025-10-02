# Railway Reservation System

## Table of Contents

- [Project Description](#project-description)
- [Features List](#features-list)
- [Prerequisites](#prerequisites)
- [Installation/Setup Steps](#installationsetup-steps)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Code Structure](#code-structure)
- [Assumptions and Constraints](#assumptions-and-constraints)
- [Evaluation Criteria Met](#evaluation-criteria-met)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

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

## Future Enhancements

Drawing inspiration from real-world railway reservation platforms like IRCTC (Indian Railway Catering and Tourism Corporation), MakeMyTrip, and Ixigo, the system can be expanded to provide a more comprehensive and user-friendly experience. Potential enhancements include:

- **Multiple Trains and Routes**: Add support for different trains with varying capacities, routes, departure/arrival times, and classes (e.g., AC, Non-AC). This would involve creating a 'trains' table and linking passengers to specific trains, similar to how IRCTC allows booking across multiple trains.
- **User Accounts and Registration**: Implement user registration and login instead of hardcoded admin credentials, enabling personalized bookings and history tracking, akin to MakeMyTrip's user profiles.
- **Payment Integration**: Integrate payment gateways for secure online payments, refunds, and cancellations, mirroring Ixigo's payment features.
- **Advanced Search and Filtering**: Allow searching tickets by date, train, or passenger details, and filtering passenger lists by status or booking date.
- **Notifications and Alerts**: Add email/SMS notifications for booking confirmations, cancellations, and waiting list updates, as seen in IRCTC's alert system.
- **Mobile/Web Interface**: Develop a web-based or mobile app interface using frameworks like Flask/Django for web or React Native for mobile, enhancing accessibility like MakeMyTrip and Ixigo.
- **Reporting and Analytics**: Add admin features for generating reports on bookings, revenue, and occupancy, useful for railway operators.
- **Concurrency and Scalability**: Implement threading or asynchronous operations to handle multiple users simultaneously, with database locking for data integrity.
- **API Development**: Create RESTful APIs for integration with third-party services, enabling features like external booking aggregators.

These enhancements would transform the system into a full-fledged railway reservation platform, improving efficiency and user satisfaction.

## Contributing

We welcome contributions from the community to enhance the Railway Reservation System! Whether you're a developer, designer, or tester, there are many ways to get involved. Inspired by open-source projects and platforms like IRCTC, MakeMyTrip, and Ixigo, which continuously evolve based on user feedback and technological advancements, this project aims to grow through collaborative efforts.

### How to Contribute

1. **Fork the Repository**: Create a fork of the project on GitHub.
2. **Create a Feature Branch**: Work on your changes in a dedicated branch (e.g., `feature/add-payment-integration`).
3. **Make Changes**: Implement your feature or fix, ensuring code quality and adherence to the existing modular architecture.
4. **Test Thoroughly**: Run existing tests and add new ones if necessary.
5. **Submit a Pull Request**: Describe your changes, why they're needed, and how they align with the project's goals.

### Areas for Contribution

- **New Features**: Implement any of the future enhancements listed above, such as multiple trains, user accounts, or payment integration.
- **UI/UX Improvements**: Enhance the console interface or develop a graphical/web interface.
- **Database Optimizations**: Improve query performance, add indexes, or support other databases (e.g., MySQL).
- **Testing and Quality Assurance**: Expand the test suite, add unit tests, integration tests, or automated testing frameworks.
- **Documentation**: Update README, add code comments, or create user guides.
- **Security Enhancements**: Implement secure authentication, data encryption, or vulnerability fixes.
- **Bug Fixes**: Identify and resolve issues in existing functionality.
- **Localization**: Add support for multiple languages, similar to international platforms like MakeMyTrip.

### Guidelines

- Follow PEP 8 style guidelines for Python code.
- Ensure all changes are backward-compatible where possible.
- Provide clear commit messages and PR descriptions.
- Respect the modular design: Keep UI, business logic, and data access layers separate.

By contributing, you'll help build a robust, scalable railway reservation system that could serve as a foundation for real-world applications, much like how IRCTC and Ixigo started and evolved.