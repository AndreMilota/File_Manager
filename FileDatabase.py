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


    # Given a string containing a file name with its path repended to it
    # return A dictionary containingall of the timestamp information about 
    # the file includingwhen it was created last modified and last referenced
    def get_file_timestamps(self, file_path):
        try:
            # Get the file timestamps using os.path.getctime, os.path.getmtime, and os.path.getatime
            import os
            # read the time stamps as date time objects
            data_created = os.path.getctime(file_path)
            data_modified = os.path.getmtime(file_path)
            data_accessed = os.path.getatime(file_path)

            # Convert timestamps to a more readable format (optional)
            from datetime import datetime
            data_created = datetime.fromtimestamp(data_created).strftime('%Y-%m-%d %H:%M:%S')
            data_modified = datetime.fromtimestamp(data_modified).strftime('%Y-%m-%d %H:%M:%S')
            data_accessed = datetime.fromtimestamp(data_accessed).strftime('%Y-%m-%d %H:%M:%S')

            timestamps = {
                'data_created': data_created,
                'data_modified': data_modified,
                'data_accessed': data_accessed
            }
           
            return timestamps
        except Exception as e:
            print(f"Error retrieving timestamps for {file_path}: {e}")
            return None

    # Given a string containing a file name with its path repended to it
    # return A dictionary containing all of the file attributes including its size and read only status
    # As well as all of the other parameters that the Windows operating systemmay havestored awayfor that file
    def get_file_attributes(self, file_path):
        try:
            # Get the file attributes using os.stat
            import os
            stat_info = os.stat(file_path)
            attributes = {
                'size': stat_info.st_size,
                'readonly': not bool(stat_info.st_mode & 0o222),  # Check if the file is writable
                'hidden': file_path.startswith('.'),  # Check if the file is hidden (Unix-like systems)
                'system': False,  # Placeholder for system attribute (not directly available in Python)
                'archive': False  # Placeholder for archive attribute (not directly available in Python)
            }
            return attributes
        except Exception as e:
            print(f"Error retrieving attributes for {file_path}: {e}")
            return None

        
    def close(self):
        # Close the connection when done
        self.conn.close()

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
