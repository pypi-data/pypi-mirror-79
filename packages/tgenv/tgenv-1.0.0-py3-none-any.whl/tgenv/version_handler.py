import json

from .file_handler import read_versions, version_file_exists, write_version, copy_file

def get_local_versions(filepath: str) -> str:
    """ Returns local versions
    """
    versions = read_versions(filepath)
    versions = json.loads(versions)
    return versions

def add_version(version, filepath, version_file):
    """ Adds a version to the version file

    :param version: The version to add
    :type version: string
    :param filepath: The path to the version
    :type filepath: str
    :param version_file: The file containing the versions
    :type version_file: str
    """
    versions = get_local_versions(version_file)
    versions[version] = filepath
    write_version(version_file, json.dumps(versions))

def has_version(filepath, version):
    """ Checks if version exists
    """
    versions = get_local_versions(filepath)
    try:
        version_file_exists(versions[version])
        return True
    except FileNotFoundError:
        return False
    except KeyError:
        return False

def install_version(target_path, source_path, version):
    """ Installs a version
    """
    copy_file(source_path + version, target_path)
