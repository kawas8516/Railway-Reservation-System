import psycopg2
from psycopg2 import sql

# Database connection parameters
host = 'localhost'
user = 'postgres'  # Assuming default PostgreSQL user
password = '2407'
default_db = 'postgres'  # Connect to default database to create new one
target_db = 'railway_reservation'

def create_database():
    try:
        # Connect to the default PostgreSQL database
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=default_db
        )
        conn.autocommit = True  # Required for CREATE DATABASE
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        try:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(target_db)))
            print(f"Database '{target_db}' created.")
        except psycopg2.errors.DuplicateDatabase:
            print(f"Database '{target_db}' already exists.")

        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        raise

def create_tables():
    try:
        # Connect to the target database
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=target_db
        )
        cursor = conn.cursor()

        # Create the passengers table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS passengers (
            pnr VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INTEGER NOT NULL,
            status VARCHAR(10) NOT NULL CHECK (status IN ('confirmed', 'waiting')),
            booking_date TIMESTAMP NOT NULL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'passengers' created or already exists.")

        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        raise

if __name__ == "__main__":
    try:
        create_database()
        create_tables()
        print("Database setup completed successfully.")
    except Exception as e:
        print(f"Setup failed: {e}")