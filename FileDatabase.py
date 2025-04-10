import sqlite3


class FileDatabase:
    def __init__(self, db_name):
        # Initialize the database connection and cursor
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_file_schema(self):
        # Define the schema categories as strings
        
        file_attributes = """
            id INTEGER PRIMARY KEY,
            full_path TEXT,
            name TEXT,
            extension TEXT,
            size INTEGER,
            size_on_disk INTEGER,
            data_created TEXT,
            data_modified TEXT,
            data_accessed TEXT,
            readonly INTEGER,
            hidden INTEGER,
            system INTEGER,
            archive INTEGER"""
                
        # multimedia attributes
        multimedia_attributes = """
            duration REAL,
            bitrate INTEGER,
            codec TEXT,
            framerate REAL"""
                
        # image attributes
        image_attributes = """
            image_format TEXT,
            resolution_width INTEGER,
            resolution_height INTEGER"""
                
        # audio attributes
        audio_attributes = """
            sample_rate INTEGER,
            channels INTEGER"""
                
        # agent-specific attributes
        agent_attributes = """
            first_seen TEXT,
            last_seen TEXT,
            reported_missing TEXT,
            removed_by_agent TEXT,
            moved_to TEXT,
            moved_by_agent TEXT,
            pending_deletion TEXT,
            pending_movement TEXT,
            new_location TEXT,
            source_location TEXT,
            agent_status INTEGER,
            hash TEXT,
            user_comment TEXT,
            agent_notes TEXT"""

        
        # Assemble the final schema query string
        schema_query = f"""
            CREATE TABLE IF NOT EXISTS files (
                {file_attributes},
                {multimedia_attributes},
                {image_attributes},
                {audio_attributes},
                {agent_attributes}
            )
        """
        
        # Execute the query to create the table
        self.cursor.execute(schema_query)
        self.conn.commit()

    def test_database(self):
        # Run a basic diagnostic query to check if the table exists
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files';")
        result = self.cursor.fetchone()
        
        if result:
            print("Table 'files' created successfully!")
        else:
            print("Error: Table 'files' not found.")
        
        # Test inserting a dummy row
        try:
            self.cursor.execute("""
                INSERT INTO files (full_path, name, extension, size, data_created, data_modified, data_accessed, readonly, hidden, system, archive)
                VALUES ('/path/to/file', 'example.txt', 'txt', 1234, '2025-04-07', '2025-04-07', '2025-04-07', 0, 0, 0, 1);
            """)
            self.conn.commit()
            print("Dummy row inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting dummy row: {e}")
        
        # Query the inserted row to verify it was added
        self.cursor.execute("SELECT * FROM files LIMIT 1;")
        row = self.cursor.fetchone()
        if row:
            print(f"Row inserted: {row}")
        else:
            print("No rows found in the table.")


   
        
    def close(self):
        # Close the connection when done
        self.conn.close()

    # take the time stamp information and see if is in the database
    def check_time_stamp(self, file_path, file_name, timestamps):
        # Check if the timestamps are already in the database
        self.cursor.execute("SELECT * FROM files WHERE full_path=? AND name=?", (file_path, file_name))
        result = self.cursor.fetchone()

        if result:
            print("Timestamps already exist in the database.")
            return True
        else:
            print("Timestamps not found in the database.")
            return False

    def clear_the_database(self):
        # Clear the database by dropping the table
        self.cursor.execute("DROP TABLE IF EXISTS files;")
        self.conn.commit()
        print("Database cleared.")  

# Test the FileDatabase class
# if __name__ == "__main__":
#     db = FileDatabase('test_files.db')  # Create a test database
#     db.create_file_schema()  # Create the schema
#     db.test_database()  # Perform the basic diagnostic
#     db.close()  # Close the database connection


# test to see if the file attributes and timestamps are being returned correctly
if __name__ == "__main__":
    db = FileDatabase('test_files.db')  # Create a test database
    db.create_file_schema()  # Create the schema
    db.test_database()  # Perform the basic diagnostic

    # Test file attributes and timestamps
    file_path = 'test_files.db'  # Replace with an actual file path for testing
    timestamps = db.get_file_timestamps(file_path)
    attributes = db.get_file_attributes(file_path)

    print(f"Timestamps: {timestamps}")
    print(f"Attributes: {attributes}")

    db.close()  # Close the database connection
