import os

import pkg_resources


def get_path_of_data_file(data_file):

    path = get_path_of_data_dir()

    file_path = os.path.join(path, data_file)

    return file_path


def get_path_of_data_dir():
    file_path = pkg_resources.resource_filename("vangogh", "data")

    return file_path
