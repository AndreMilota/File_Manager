# this file loads the directoris into the file database
import sqlite3
import Dir_Reader
import FileDatabase
import mimetypes


# def is_media_file(file_path):
#     mimetype, _ = mimetypes.guess_type(file_path)
#     return mimetype and mimetype.startswith(('audio', 'video', 'image'))

def load_file_data(file_path, db_cursor):
    try:
        file_data = Dir_Reader.get_all_file_data(file_path)
        if not file_data:
            print(f"Skipping file due to missing data: {file_path}")
            return

        # Prepare columns and values for insertion
        columns = ', '.join(file_data.keys())
        placeholders = ', '.join('?' for _ in file_data)
        values = tuple(file_data.values())

        query = f"INSERT INTO files ({columns}) VALUES ({placeholders})"
        db_cursor.execute(query, values)

        print(f"Inserted data for {file_path} into the database.")
        print (f"File data: {file_data}")

    except Exception as e:
    
        print(f"Error processing {file_path}: {e}")
        print (f"File data: {file_data}")

def load_directory_data(directory_path, db_cursor):
    """ Get all files in the directory and its subdirectories """
    file_paths = Dir_Reader.get_all_files_in_directory(directory_path)

    # Load each file's data into the database
    for file_path in file_paths:
        load_file_data(file_path, db_cursor)


# test load directory data

if __name__ == "__main__":
    from FileDatabase import FileDatabase

    db_path = 'file_data.db'

    try:
        # Clear and recreate the database
        db = FileDatabase(db_path)
        db.conn.execute("DROP TABLE IF EXISTS files")
        db.conn.commit()

        db.create_file_schema()

        cursor = db.conn.cursor()

        # Load directory data into the database
        load_directory_data('C:/Users/owner/Downloads/', cursor)

        # Commit changes after loading data
        db.conn.commit()

        # Print the contents of the database
        cursor.execute("SELECT * FROM files")
        for row in cursor.fetchall():
            print(row)

    except Exception as e:
        print(f"An error occurred in the print: {e}")
        db.conn.rollback()

    finally:
        # Make sure everything is properly closed
        try:
            cursor.close()
        except Exception:
            pass

        try:
            db.conn.close()
        except Exception:
            pass

#
# Example usage
# if __name__ == "__main__":
#     # clear the database
#     db = FileDatabase.FileDatabase('file_data.db')
#     db.conn.execute("DROP TABLE IF EXISTS files")
#     db.conn.commit()
#     db.conn.close()
#     # Connect to the database
#     db = FileDatabase.FileDatabase('file_data.db')
#     db.create_file_schema()

#     cursor = db.conn.cursor()
#     # Load file data into the database
#     load_file_data('C:/Users/owner/VS code projects/File_Manager/FileDatabase.py', cursor)
#     load_file_data('C:/Users/owner/Downloads/Stripsearch - Hey Kid (1982) [ ezmp3.cc ].mp3', cursor)

#     # print the contents of the database
#     cursor.execute("SELECT * FROM files")
#     rows = cursor.fetchall() # fetch all rows from the cursor
#     for row in rows:
#         print(row)
#     # Close the cursor and database connection
#     cursor.close()

#     # Close the database connection
#     db.conn.close()
