"""
Python wrapper for NDC.

http://euee.web.fc2.com/tool/nd.html
"""

import platform
import subprocess

from datetime import datetime
from os.path import expanduser


class NDCError(Exception):
    pass


class NDCVersionException(NDCError):
    pass


class NDCRuntimeError(NDCError):
    pass


class NDCPermissionError(NDCRuntimeError):
    pass


class NDCFileNotFoundError(NDCRuntimeError):
    pass


class NDCInvalidImagePathError(NDCRuntimeError):
    pass


class NDCInvalidPartitionError(NDCRuntimeError):
    pass


class NDC:
    """
    NDC binary wrapper.

    For all methods:

    * `path` refers to a path within the disk image.
    * `src` and `dest` are on the native file system.
    * `image` is a path to a disk image.
    """
    SUPPORTED_VERSIONS = [
        'NDC Ver.0 alpha06',
    ]
    DELIMITER = '\t'
    ERRORS = {
        'イメージのオープンに失敗しました。': NDCPermissionError,
        '指定のフォルダが存在しません。': NDCFileNotFoundError,
        'イメージパスが不正です。': NDCInvalidImagePathError,
        'パーティション番号が不正です。': NDCInvalidPartitionError,
    }

    def __init__(self, bin='ndc'):
        self.bin = expanduser(bin)
        self.__validate_bin_version()

    def __validate_bin_version(self):
        ndc_output = subprocess.check_output(self.bin)
        if self.__is_windows():
            decoded_output = ndc_output.decode('shift-jis')
        else:
            decoded_output = ndc_output.decode()
        version = decoded_output.splitlines().pop(0)
        if version not in self.SUPPORTED_VERSIONS:
            raise NDCVersionException('Unsupported version: %s' % version)
        self.version = version

    def __run(self, cmd):
        try:
            result = self.__decode(subprocess.check_output(cmd)).splitlines()
            result.pop()  # success message
            return result
        except subprocess.CalledProcessError as e:
            error_msg = self.__decode(e.output).strip()
            error_msg = error_msg[:error_msg.index('。') + 1]
            raise self.ERRORS[error_msg](error_msg)

    def __is_windows(self):
        return platform.system() == 'Windows'

    def __decode(self, output):
        if self.__is_windows():
            return output.decode('shift-jis')
        else:
            return output.decode()

    def __parse(self, line):
        """Helper function for parsing output from list, and find."""
        if self.__is_windows():
            TIMESTAMP_FMT = '%Y/%m/%d %H:%M:%S'
        else:
            TIMESTAMP_FMT = '%a %b %d %H:%M:%S %Y'
        args = line.split(self.DELIMITER)
        args[-1] = datetime.strptime(args[-1], TIMESTAMP_FMT)
        return tuple(args)

    def list(self, image, path='', partition=0):
        SKIP = ['.', '..']
        cmd = [
            self.bin,
            expanduser(image),
            str(partition),
            path,
        ]
        return [self.__parse(args)
                for args in self.__run(cmd)
                if args[0] not in SKIP]

    def find(self, image, pattern, path='', partition=0):
        cmd = [
            self.bin,
            'F',
            expanduser(image),
            str(partition),
            path,
            pattern,
        ]
        result = self.__run(cmd)
        return self.__parse(result[0]) if result else None

    def find_all(self, image, pattern, path='', partition=0):
        cmd = [
            self.bin,
            'FA',
            expanduser(image),
            str(partition),
            path,
            pattern,
        ]
        return [self.__parse(line) for line in self.__run(cmd)]

    def get(self, image, path, dest=None, partition=0):
        cmd = [
            self.bin,
            'G',
            expanduser(image),
            str(partition),
            path,
            dest,
        ]
        self.__run(cmd)

    def put(self, image, src, path, partition=0):
        cmd = [
            self.bin,
            'P',
            expanduser(image),
            str(partition),
            src,
            path,
        ]
        self.__run(cmd)

    def put_directory(self, image, directory, path='', partition=0):
        cmd = [
            self.bin,
            'PD',
            expanduser(image),
            str(partition),
            directory,
            path,
        ]
        self.__run(cmd)

    def delete(self, image, path, partition=0):
        cmd = [
            self.bin,
            'D',
            expanduser(image),
            str(partition),
            path,
        ]
        self.__run(cmd)
