import os
from setuptools import setup, find_packages


def get_directories(path, prefix=''):
    """
    :param path:
    :param prefix:
    :return:
    """
    result = []
    for item in os.scandir(path):
        if item.is_dir():
            result.append(prefix + item.name)
            result += get_directories(item.path, prefix + item.name + '.')
    return result


def get_package_data(root_dir, file_types):
    """
    :param root_dir:
    :param file_types:
    :return:
    """
    directories = get_directories(root_dir)
    diz = {}
    for directory in directories:
        diz[directory] = file_types
    return diz


def read_version():
    with open("../../../VERSION", "r", encoding='utf-8') as version_file:
        return version_file.read().strip().replace('-', '.')


setup(
    name="common_package",
    version=read_version(),
    packages=find_packages(),
    include_package_data=True,
    package_data=get_package_data(os.getcwd(), ['*.sql'])
)
