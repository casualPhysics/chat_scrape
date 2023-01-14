from pathlib import Path
import os
import zipfile
import io


def write_bytes_file(path, file_data_tmp):
    with open(path, 'wb') as f:
        f.write(file_data_tmp)


def unzip_into_directory(zip_file, raw_data_directory):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(raw_data_directory)


def scan_files_directory(directory_string, applier_function):
    directory = os.fsencode(directory_string)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".zip") or filename.endswith(".py"):
            print(filename)
            applier_function(f"{directory_string}/{filename}")
            continue
        else:
            continue


def reparse_filename(string):
    return string.lower().replace(' ', '_').replace('.zip', '')


def unzip_files(directory_string, target_directory):
    scan_files_directory(directory_string, lambda x: unzip_into_directory(x, target_directory))


def unzip_file_into_directory(zip_file_path, target_directory):
    """
    Unzip a zip file from a path into a directory
    nested in a target directory
    :param zip_file: The relative path of the zip file
    :param target_directory: The target directory
    :return: a status code
    """
    nested_dir = f"{target_directory}/" \
                 f"{reparse_filename(os.path.basename(zip_file_path))}"
    try:
        Path(nested_dir).mkdir(parents=True, exist_ok=True)
        unzip_into_directory(zip_file_path, nested_dir)
        return 1
    except RuntimeError:
        Exception("Unable to write to dictionary")


def unzip_files_in_dir_to_dir(source_dir, target_dir):
    """
    Take zip files in a directory and unzip them into
    another directory.
    :param source_dir:
    :param target_dir:
    :return:
    """
    scan_files_directory(source_dir,
                         lambda x: unzip_file_into_directory(x, target_dir))


def read_txt_file_from_zip_buffer(file_buffer):
    z = zipfile.ZipFile(io.BytesIO(file_buffer))
    text_string = z.read(z.infolist()[0])
    z.extractall()
    z.close()
    return text_string
