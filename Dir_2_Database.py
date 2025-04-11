# this file loads the directoris into the file database
import sqlite3
import Dir_Reader
import FileDatabase




# load all the data for a file into a database row 
# this uses the files in dir_Reader to extract the data from the file
def load_file_data(file_path, db_cursor):
    # Extract file attributes

    # break the file path file name and extension into out of the file path
    # this is done to make it easier to extract the file attributes
    path = file_path.replace('\\', '/')
    extention = path.split('/')[-1].split('.')[-1]
    file_name = path.split('/')[-1].split('.')[0]   
    path = '/'.join(path.split('/')[:-1])
    # put them into a dictionary to make it easier to extract the file attributes
    idenitifier = {
        'name': file_name,
        'extension': extention,
        'full_path': path
    }

    file_attributes = Dir_Reader.get_file_attributes(file_path)
    multimedia_attributes = Dir_Reader.get_media_metadata(file_path)
    all_attributes = {**idenitifier, **file_attributes, **multimedia_attributes }

    sql = """
    INSERT INTO files (full_path, name, extension, size, size_on_disk,
    data_created, data_modified, data_accessed, readonly, hidden,
    system, archive, duration, bitrate, codec, framerate,
    image_format, resolution_width, resolution_height,
    sample_rate, channels)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?)"""

    # for debugging purposes, print all the attributes
    print("Inserting file data into database:")
    for key, value in all_attributes.items():
        print(f"{key}: {value}")

    db_cursor.execute(sql, (
        all_attributes.get('full_path'),  # Full path of the file
        all_attributes.get('name'),  # Name of the file
        all_attributes.get('extension'),  # File extension
        all_attributes.get('size', 0),  # Size, default 0 if not found
        all_attributes.get('size_on_disk', 0),  # Size on disk, default 0 if not found
        all_attributes.get('data_created'),  # Date created
        all_attributes.get('data_modified'),  # Date modified
        all_attributes.get('data_accessed'),  # Date accessed
        int(all_attributes.get('readonly', 0)),  # Readonly flag (convert to int)
        int(all_attributes.get('hidden', 0)),  # Hidden flag (convert to int)
        int(all_attributes.get('system', 0)),  # System flag (convert to int)
        int(all_attributes.get('archive', 0)),  # Archive flag (convert to int)
        all_attributes.get('duration'),  # Duration (can be None or float)
        all_attributes.get('bitrate'),  # Bitrate (can be None or integer)
        all_attributes.get('codec'),  # Codec (can be None)
        all_attributes.get('framerate'),  # Framerate (can be None or float)
        all_attributes.get('image_format'),  # Image format (can be None)
        all_attributes.get('resolution_width'),  # Resolution width (can be None or integer)
        all_attributes.get('resolution_height'),  # Resolution height (can be None or integer)
        all_attributes.get('sample_rate'),  # Sample rate (can be None or integer)
        all_attributes.get('channels')  # Channels (can be None or integer)
    ))

    db_cursor.connection.commit()

def load_directory_data(directory_path, db_cursor):
    """ Get all files in the directory and its subdirectories """
    file_paths = Dir_Reader.get_all_files(directory_path)

    # Load each file's data into the database
    for file_path in file_paths:
        load_file_data(file_path, db_cursor)


# test load directory data
if __name__ == "__main__":
    # clear the database
    db = FileDatabase.FileDatabase('file_data.db')
    db.conn.execute("DROP TABLE IF EXISTS files")
    db.conn.commit()
    db.conn.close()
    # Connect to the database
    db = FileDatabase.FileDatabase('file_data.db')
    db.create_file_schema()

    cursor = db.conn.cursor()

    # Load directory data into the database
    load_directory_data('C:/Users/owner/Downloads', cursor)

    # print the contents of the database
    cursor.execute("SELECT * FROM files")
    rows = cursor.fetchall()  # fetch all rows from the cursor
    for row in rows:
        print(row)

    # Close the cursor and database connection
    cursor.close()
    db.conn.close()

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
