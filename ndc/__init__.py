"""
Python wrapper for NDC.

http://euee.web.fc2.com/tool/nd.html
"""

import platform
import subprocess

from dateutil.parser import parse as dateparse
from os import mkdir
from os.path import expanduser, join


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


class NDCFileStorageFailureError(NDCRuntimeError):
    pass


class NDCInvalidSourcePathError(NDCRuntimeError):
    pass


class NDCInvalidDestinationPathError(NDCRuntimeError):
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
        'NDC Ver.0 alpha06b',
        'NDC Ver.0 alpha06',
    ]
    DELIMITER = '\t'
    DIR = '<DIR>'
    ERRORS = {
        'イメージのオープンに失敗しました。': NDCPermissionError,
        '指定のフォルダが存在しません。': NDCFileNotFoundError,
        'イメージパスが不正です。': NDCInvalidImagePathError,
        'パーティション番号が不正です。': NDCInvalidPartitionError,
        'ファイルの格納に失敗しました。': NDCFileStorageFailureError,
        '読み込み元パスが存在しません。': NDCInvalidSourcePathError,
        '書き込み先フォルダが存在しません。': NDCInvalidDestinationPathError,
    }

    def __init__(self, bin='ndc'):
        self.bin = expanduser(bin)
        self.__configure_platform()
        self.__validate_bin_version()

    def __configure_platform(self):
        if platform.system() == 'Windows':
            self.encoding = 'shift-jis'
        else:
            self.encoding = 'utf-8'

    def __validate_bin_version(self):
        version = (subprocess
                   .check_output(self.bin)
                   .decode(self.encoding)
                   .splitlines()
                   .pop(0))
        if version not in self.SUPPORTED_VERSIONS:
            raise NDCVersionException('Unsupported version: %s' % version)
        self.version = version

    def __run(self, *args):
        cmd = [self.bin] + list(args)
        try:
            result = (subprocess
                      .check_output(cmd)
                      .decode(self.encoding)
                      .splitlines())
            result.pop()  # success message
            return result
        except subprocess.CalledProcessError as e:
            error_msg = e.output.decode(self.encoding).strip()
            error_msg = error_msg[:error_msg.index('。') + 1]
            raise self.ERRORS[error_msg](error_msg)

    def __parse(self, line):
        """Helper function for parsing output from list, and find."""
        args = line.split(self.DELIMITER)
        args[-1] = dateparse(args[-1])
        return tuple(args)

    def list(self, image, path='', partition=0):
        SKIP = ['.', '..']
        args = [
            expanduser(image),
            str(partition),
            path,
        ]
        return [self.__parse(args)
                for args in self.__run(*args)
                if args[0] not in SKIP]

    def find(self, image, pattern, path='', partition=0):
        result = self.__run(
            'F',
            expanduser(image),
            str(partition),
            path,
            pattern,
        )
        return self.__parse(result[0]) if result else None

    def find_all(self, image, pattern, path='', partition=0):
        args = [
            'FA',
            expanduser(image),
            str(partition),
            path,
            pattern,
        ]
        return [self.__parse(line) for line in self.__run(*args)]

    def get(self, image, path, dest='.', partition=0):
        self.__run(
            'G',
            expanduser(image),
            str(partition),
            path,
            dest,
        )

    def put(self, image, src, path, partition=0):
        self.__run(
            'P',
            expanduser(image),
            str(partition),
            expanduser(src),
            path,
        )

    def put_directory(self, image, directory, path='', partition=0):
        self.__run(
            'PD',
            expanduser(image),
            str(partition),
            directory,
            path,
        )

    def delete(self, image, path, partition=0):
        self.__run(
            'D',
            expanduser(image),
            str(partition),
            path,
        )

    def walk(self, image, top=''):
        """
        A generator that walks the files of an image, starting from path `top`.
        """
        results = self.list(image, top)[1:]  # skip volume

        dirpaths = []
        filenames = []
        for name, _, name_type, _ in results:
            if name_type == self.DIR:
                dirpaths.append(name)
            else:
                filenames.append(name)

        yield (top, dirpaths, filenames)

        for dirpath in dirpaths:
            yield from self.walk(image, join(top, dirpath))

    def extract(self, image, destination='.'):
        """
        Extract the contents of `image` to `destination`.
        """
        for dirpath, dirnames, filenames in self.walk(image):
            for filename in filenames:
                self.get(image, join(dirpath, filename), join(destination, dirpath))
            for dirname in dirnames:
                mkdir(join(destination, dirpath, dirname))
