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
        
        # Multimedia attributes (covering video and audio)
        multimedia_attributes = """
            duration REAL,
            bitrate INTEGER,
            codec TEXT,
            resolution_width INTEGER,
            resolution_height INTEGER,
            framerate REAL,
            sample_rate INTEGER,
            channels INTEGER"""
        
        # Image attributes (specific to images)
        image_attributes = """
            image_format TEXT"""
        
        # Audio attributes (specific to audio, could overlap with multimedia)
        audio_attributes = """
            bitrate INTEGER,
            duration REAL,
            codec TEXT"""
        
        # Agent attributes (track agent-specific interactions)
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
            user_comment TEXT,
            agent_notes TEXT,
            hash TEXT,
            agent_status INTEGER"""
        
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

# Test the FileDatabase class
if __name__ == "__main__":
    db = FileDatabase('test_files.db')  # Create a test database
    db.create_file_schema()  # Create the schema
    db.test_database()  # Perform the basic diagnostic
    db.close()  # Close the database connection

