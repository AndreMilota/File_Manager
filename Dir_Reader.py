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
            encoding='utf-8'
        )

        if result.returncode != 0:
            print(f"ffprobe failed for {file_path}: {result.stderr}")
            return None

        metadata = json.loads(result.stdout)

        # Initialize fields with default None
        data = {
            'duration': None,
            'bitrate': None,
            'codec': None,
            'framerate': None,
            'image_format': None,
            'resolution_width': None,
            'resolution_height': None,
            'sample_rate': None,
            'channels': None
        }

        # Extract from 'format'
        fmt = metadata.get('format', {})
        if 'duration' in fmt:
            try:
                data['duration'] = float(fmt['duration'])
            except ValueError:
                pass
        if 'bit_rate' in fmt:
            try:
                data['bitrate'] = int(fmt['bit_rate'])
            except ValueError:
                pass
        if 'format_name' in fmt:
            data['image_format'] = fmt['format_name']

        # Extract from 'streams'
        for stream in metadata.get('streams', []):
            codec_type = stream.get('codec_type')

            # Use first codec name found
            if data['codec'] is None:
                data['codec'] = stream.get('codec_name')

            # For video streams
            if codec_type == 'video':
                if stream.get('width'):
                    data['resolution_width'] = stream.get('width')
                if stream.get('height'):
                    data['resolution_height'] = stream.get('height')
                # framerate (e.g. "30000/1001")
                r_frame_rate = stream.get('r_frame_rate')
                if r_frame_rate and r_frame_rate != '0/0':
                    try:
                        num, den = map(float, r_frame_rate.split('/'))
                        data['framerate'] = num / den if den else None
                    except Exception:
                        pass

            # For audio streams
            elif codec_type == 'audio':
                if stream.get('sample_rate'):
                    try:
                        data['sample_rate'] = int(stream['sample_rate'])
                    except ValueError:
                        pass
                if stream.get('channels'):
                    try:
                        data['channels'] = int(stream['channels'])
                    except ValueError:
                        pass

        return data

    except Exception as e:
        print(f"Error reading media metadata from {file_path}: {e}")
        return None

# Define a set of known media extensions
MEDIA_EXTENSIONS = {'.mp3', '.mp4', '.wav', '.flac', '.mov', '.avi', '.mkv', '.webm', '.wmv', '.m4a', '.aac'}

def get_all_file_data(file_path):
    # Extract file attributes
    time_stamps = get_file_timestamps(file_path) or {}

    path = file_path.replace('\\', '/')
    extension = path.split('/')[-1].split('.')[-1]
    file_name = path.split('/')[-1].split('.')[0]   
    path = '/'.join(path.split('/')[:-1])

    identifier = {
        'name': file_name,
        'extension': extension,
        'full_path': path
    }

    file_attributes = get_file_attributes(file_path) or {}

    # Only attempt to get media metadata for valid media files
    if extension in ['mp3', 'mp4', 'avi', 'jpg', 'png', 'gif']:  # add more media types as necessary
        multimedia_attributes = get_media_metadata(file_path) or {}
    else:
        multimedia_attributes = {}

    # get the size on disk
    size_on_disk = get_size_on_disk(file_path) if os.path.isfile(file_path) else None
    if size_on_disk is not None:
        file_attributes['size_on_disk'] = size_on_disk

    all_attributes = {**identifier, **file_attributes, **multimedia_attributes, **time_stamps}

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

def test_get_media_metadata():
    # Test the function with a sample file path
    file_path = 'C:/Users/owner/Downloads/04 Cindytalk - Interruptum [Editions Mego].mp3'  # Replace with an actual file path
    file_data = get_media_metadata(file_path)
    print(f"File data for {file_path}:")
    print(file_data)

def print_all_atributes(file_path):
    # Test the function with a sample file path
    file_data = get_all_file_data(file_path)
    i = 1
    for key, value in file_data.items():
        print(f"{i}: {key}: {value}")
        i += 1

if __name__ == "__main__":
    # Test getting file data
    print_all_atributes( 'C:/Users/owner/Downloads/04 Cindytalk - Interruptum [Editions Mego].mp3' )
    # test get_all_files_in_directory
 
    # root_dir = "C:/ffmpeg"
    # subdirs = get_all_files_in_directory(root_dir)
    # print("files:")
    # for subdir in subdirs:
    #     print(subdir)
    # print("Total files:", len(subdirs))