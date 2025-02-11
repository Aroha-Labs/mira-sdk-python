import os
import base64

def get_file_content(file_path: str, max_size_mb: float = 100.0) -> str:
    # Define allowed file extensions
    TEXT_EXTENSIONS = {'.md', '.txt', '.csv'}
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
    ALLOWED_EXTENSIONS = TEXT_EXTENSIONS | IMAGE_EXTENSIONS

    # Get file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    # Check if file extension is allowed
    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type. Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed.")

    # Check file size before processing
    file_size = os.path.getsize(file_path)
    max_size_bytes = max_size_mb * 1024
    if file_size > max_size_bytes:
        raise ValueError(
            f"File size ({file_size / 1024:.2f}KB) exceeds maximum allowed size of {max_size_mb}KB"
        )

    try:
        # Handle text files
        if file_extension in TEXT_EXTENSIONS:
            with open(file_path, 'r') as file:
                return file.read()

        # Handle image files
        else:
            with open(file_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")
