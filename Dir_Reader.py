# this reads the directory infomation including file paramters 
import ctypes
from ctypes import wintypes  
import subprocess
import json
import os

 # Given a string containing a file name with its path repended to it
    # return A dictionary containingall of the timestamp information about 
    # the file includingwhen it was created last modified and last referenced
def get_file_timestamps(file_path):
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
def get_file_attributes(file_path):
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

def get_size_on_disk(file_path):
    GetCompressedFileSizeW = ctypes.windll.kernel32.GetCompressedFileSizeW
    GetCompressedFileSizeW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.DWORD)]
    GetCompressedFileSizeW.restype = wintypes.DWORD

    high_word = wintypes.DWORD(0)
    low_word = GetCompressedFileSizeW(file_path, ctypes.byref(high_word))

    if low_word == 0xFFFFFFFF and ctypes.GetLastError() != 0:
        raise ctypes.WinError()
    
    return (high_word.value << 32) + low_word

def get_media_metadata(file_path):
    try:
        # Call ffprobe to get media metadata as JSON
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                file_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8'  # Explicitly set encoding to avoid UnicodeDecodeError
        )

        # Check for ffprobe failure
        if result.returncode != 0:
            print(f"ffprobe failed for {file_path}: {result.stderr}")
            return None

        # Parse the JSON output
        metadata = json.loads(result.stdout)

        # Initialize variables
        duration = None
        width = None
        height = None
        codec_name = None

        # Extract duration and format info
        if 'format' in metadata and 'duration' in metadata['format']:
            try:
                duration = float(metadata['format']['duration'])
            except ValueError:
                duration = None

        # Find the first video stream
        if 'streams' in metadata:
            for stream in metadata['streams']:
                if stream.get('codec_type') == 'video':
                    width = stream.get('width')
                    height = stream.get('height')
                    codec_name = stream.get('codec_name')
                    break

        return {
            'duration': duration,
            'width': width,
            'height': height,
            'codec': codec_name
        }

    except Exception as e:
        print(f"Error reading media metadata for {file_path}: {e}")
        return None

    except Exception as e:
        print(f"Error extracting metadata for {file_path}: {e}")
        return None

def get_all_file_data(file_path):
    # Extract file attributes

    # break the file path file name and extension into out of the file path
    # this is done to make it easier to extract the file attributes
    path = file_path.replace('\\', '/')
    extention = path.split('/')[-1].split('.')[-1]
    file_name = path.split('/')[-1].split('.')[0]   
    path = '/'.join(path.split('/')[:-1])
    # put them into a dictionary to make it easier to extract the file attributes
    identifier  = {
        'name': file_name,
        'extension': extention,
        'full_path': path
    }

    file_attributes = get_file_attributes(file_path) or {}
    multimedia_attributes = get_media_metadata(file_path) or {}
    all_attributes = {**identifier, **file_attributes, **multimedia_attributes }

    return all_attributes

def get_subdirectories(root_dir):
    subdirs = []
    for dirpath, dirnames, _ in os.walk(root_dir, followlinks=False):
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            subdirs.append(full_path)
    return subdirs

def get_all_files_in_directory(root_dir):
    """ get all the full paths of the files in the directory tree """
    all_files = []
    for dirpath, _, filenames in os.walk(root_dir, followlinks=False):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            all_files.append(full_path)
    return all_files

if __name__ == "__main__":
    # test get_all_files_in_directory
 
    root_dir = "C:/ffmpeg"
    subdirs = get_all_files_in_directory(root_dir)
    print("files:")
    for subdir in subdirs:
        print(subdir)
    print("Total files:", len(subdirs))