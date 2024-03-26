#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from kdp_catalog_manager.exceptions.exception import FileNotExistsError, \
    ReadFileError, WriteFileError
from kdp_catalog_manager.utils.log import log


class FileUtils(object):

    @staticmethod
    def check_file_exists(file, log_err=True):
        if not os.path.lexists(file):
            if log_err:
                log.debug("File {} not exists!".format(file))
            return False
        else:
            return True

    def read_file(self, file):
        if self.check_file_exists(file):
            try:
                with open(file) as f:
                    rtn = f.read()
                return rtn
            except IOError as e:
                log.exception(e)
                raise ReadFileError(file)
        else:
            log.warning("File {} not exists".format(file))
            raise FileNotExistsError(file)

    @staticmethod
    def write_file(content, target_file):
        try:
            with open(target_file, 'w') as f:
                f.write(content)
        except Exception as err:
            log.error(str(err))
            raise WriteFileError(target_file)
