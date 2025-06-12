import os
import zipfile

def unzip_all(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(source_dir):
        if item.lower().endswith('.zip'):
            zip_path = os.path.join(source_dir, item)
            extract_folder = os.path.join(dest_dir, os.path.splitext(item)[0])

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                os.makedirs(extract_folder, exist_ok=True)
                zip_ref.extractall(extract_folder)
                print(f'Extracted: {zip_path} to {extract_folder}')

# Example usage
source_directory = '/path/to/zip/folder'
destination_directory = '/path/to/output/folder'
unzip_all(source_directory, destination_directory)