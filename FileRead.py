import charset_normalizer
from config import MIN_CONFIDENCE, DETECTION_BUFFER_SIZE


def detect_encoding(file_path: str) -> str | None:
    """
    Detects the encoding of the file by reading the first few bytes.

    Args:
        file_path: The path of the file.

    Returns:
        The detected encoding (e.g., 'utf-8', 'latin-1') as a string,
        or None if:
        - The file is not found.
        - The file is empty.
        - Encoding detection fails or the confidence level is below MIN_CONFIDENCE.
        - An unexpected error occurs during the process.
    """
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read(DETECTION_BUFFER_SIZE)
            if not raw_data: 
                print(f"Empty file: {file_path}")
                return None 
                
            # charset_normalizer használata chardet helyett
            detection_result = charset_normalizer.detect(raw_data)
            
            if detection_result and detection_result['encoding'] and\
               detection_result['confidence'] > MIN_CONFIDENCE:
                return detection_result['encoding']
            else:
                confidence = detection_result.get('confidence', 0) if\
                      detection_result else 0
                print(f"Encoding detection confidence ({confidence}) is below "
                      f"threshold ({MIN_CONFIDENCE}) or encoding not found for\
                         file: {file_path}")
                return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred during encoding detection for file \
              {file_path}: {e}")
        return None


def read_file_content(file_path: str) -> str | None:
    """
    Reads a file with automatically detected encoding.

    Args:
        file_path: The path of the file.

    Returns:
        The content of the file as a string, or None if:
        - The file is not found.
        - The file is empty (leading to failed encoding detection).
        - Encoding detection fails or is unreliable.
        - A UnicodeDecodeError occurs when reading with the detected encoding.
        - Any other unexpected error occurs during file access or reading.
    """
    encoding = detect_encoding(file_path)
    if encoding is None:
        print(f"Could not detect encoding for file: {file_path}")
        return None

    try:
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        return content

    except UnicodeDecodeError:
        print(f"UnicodeDecodeError: Could not decode file {file_path} with detected encoding {encoding}")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while reading file {file_path}: {e}")
        return None
