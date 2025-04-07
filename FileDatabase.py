import os
import sqlite3
from pathlib import Path
from datetime import datetime

DB_FILENAME = "file_inventory.db"

class FileDatabase:
    def __init__(self, db_path=DB_FILENAME):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_schema()

    def _create_schema(self):
        # schema sub elements 
        # general file attributes

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
            archive INTEGER,"""
         
        # multimedia attributes
        multimedia_attributes = """
            duration REAL,
            bitrate INTEGER,
            codec TEXT,
            resolution_width INTEGER,
            resolution_height INTEGER,
            framerate REAL,
            sample_rate INTEGER,
            channels INTEGER,"""
        
        # image attributes
        image_attributes = """
            image_mode TEXT,
            image_format TEXT,"""
        
        # audio attributes
        audio_attributes = """
            metadata_tags TEXT,
            user_comment TEXT,"""
            
        # history attributes
        history_attributes = """
            first_seen TEXT,
            last_seen TEXT,
            reported_missing TEXT,
            removed_by_agent TEXT,
            moved_to TEXT,
            moved_by_agent TEXT,
            pending_deletion TEXT,
            pending_movment TEXT,
            new_location TEXT,
            source_location TEXT,"""
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                full_path TEXT,
                name TEXT,
                extension TEXT,
                size INTEGER,
                created TEXT,
                modified TEXT,
                accessed TEXT,
                readonly INTEGER,
                hidden INTEGER,
                system INTEGER,
                archive INTEGER,
                duration REAL,
                bitrate INTEGER,
                codec TEXT,
                resolution_width INTEGER,
                resolution_height INTEGER,
                framerate REAL,
                sample_rate INTEGER,
                channels INTEGER,
                image_mode TEXT,
                image_format TEXT,
                metadata_tags TEXT,
                user_comment TEXT,
                agent_notes TEXT,
                tags TEXT,
                group_id TEXT,
                status TEXT,
                confidence REAL,
                label TEXT,
                scanned_at TEXT,
                hash TEXT,
                hash_updated_at TEXT,
                removed_at TEXT,
                moved_to TEXT
            )
        """)
        self.conn.commit()

    def clear(self):
        self.cursor.execute("DROP TABLE IF EXISTS files")
        self.conn.commit()
        self._create_schema()

    def scan_directory(self, path):
        now = datetime.utcnow().isoformat()
        for root, _, files in os.walk(path):
            for fname in files:
                fpath = os.path.join(root, fname)
                stat = os.stat(fpath)
                name = Path(fname).stem
                ext = Path(fname).suffix.lower()
                self.cursor.execute("""
                    INSERT INTO files (
                        full_path, name, extension, size, created,
                        modified, accessed, readonly, hidden, system, archive,
                        scanned_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fpath, name, ext, stat.st_size,
                    datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    datetime.fromtimestamp(stat.st_atime).isoformat(),
                    int(not os.access(fpath, os.W_OK)),  # readonly
                    0, 0, 0,  # hidden/system/archive to be handled later
                    now
                ))
        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = FileDatabase()
    db.scan_directory(".")  # Change this to your desired path
    db.close()
