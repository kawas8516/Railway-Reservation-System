# Railway Reservation System Design Document

## Overall System Architecture

The system follows a modular design using Python with psycopg2 for PostgreSQL interaction. It is structured into the following modules:

- **main.py**: Entry point of the application. Handles the main menu and orchestrates calls to other modules.
- **database.py**: Contains DatabaseManager class for managing database connections, queries, and operations. Methods for connecting to PostgreSQL, executing CRUD operations, and handling transactions.
- **passenger.py**: Contains PassengerManager class for business logic. Methods include book_ticket(), cancel_ticket(), search_by_pnr(), display_all_passengers(), view_available_seats().
- **ui.py**: Contains UIManager class for user interface elements. Methods for menu display, input validation, error handling, user feedback, and admin authentication.
- **config.py**: Stores configuration constants like database credentials (host: localhost, password: 2407).

Classes are used for encapsulation and maintainability, with methods grouped by responsibility.

## Database Schema

Database: PostgreSQL managed via pgAdmin.

Tables:

- **passengers**
  - pnr: VARCHAR(10) PRIMARY KEY (unique identifier)
  - name: VARCHAR(100) NOT NULL
  - age: INTEGER NOT NULL
  - status: VARCHAR(10) NOT NULL (values: 'confirmed', 'waiting')
  - booking_date: TIMESTAMP NOT NULL (date and time of booking)

Relationships: None (single table design for simplicity).

Additional considerations: A separate table for train capacity could be added for scalability, e.g., **trains** with capacity INTEGER, but for this scope, capacity is handled in code (max 100 passengers).

## UI Flow Description

The application is menu-driven with console-based interface.

1. **Startup**: Prompt for admin authentication (username/password).
2. **Main Menu**:
   - Book Ticket
   - Cancel Ticket
   - Search by PNR
   - Display All Passengers
   - View Available Seats
   - Exit
3. **Book Ticket**: Input name, age. Assign PNR, status based on availability (confirmed if <100, waiting if >=100).
4. **Cancel Ticket**: Input PNR, remove passenger, update availability.
5. **Search by PNR**: Input PNR, display details.
6. **Display All**: List all passengers with details.
7. **View Available Seats**: Display the number of available seats (100 - current passenger count).
8. **Error Handling**: Validate inputs (e.g., age >0, name not empty), show feedback messages.
8. **Feedback**: Success/error messages after operations.

Flow diagram (text-based):

```
Start -> Admin Auth -> Main Menu
Main Menu -> Book Ticket -> Validate Input -> Assign Status -> Save to DB -> Feedback -> Main Menu
Main Menu -> Cancel Ticket -> Validate PNR -> Remove from DB -> Feedback -> Main Menu
Main Menu -> Search by PNR -> Validate PNR -> Query DB -> Display -> Main Menu
Main Menu -> Display All -> Query DB -> Display List -> Main Menu
Main Menu -> View Available Seats -> Query DB -> Display Count -> Main Menu
Main Menu -> Exit -> End
```

## Assumptions and Constraints

- **Assumptions**:
  - Single train with fixed capacity of 100 passengers.
  - PNR is auto-generated unique string.
  - Admin authentication is simple (hardcoded credentials).
  - No concurrent users; single-threaded.
  - PostgreSQL is pre-installed and configured.

- **Constraints**:
  - Handle at least 100 passengers (status logic).
  - Scalable: Modular design allows adding features like multiple trains.
  - Maintainable: Separate concerns, no global state.
  - Python 3.x required.
  - Must handle database connection failures gracefully (e.g., retry logic, user feedback).
  - Must support concurrent users (e.g., use threading or database locking for safe operations).