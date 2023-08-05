import os
from os import listdir
from os.path import isfile

from pollect.sources import Log
from pollect.sources.Source import Source
from pollect.writers.Writer import Writer, DryRunWriter


class ObjectFactory:
    """
    Generic factory for creating objects
    """

    def __init__(self, module_name: str):
        self._module = module_name
        self._modules = self._get_modules()

    def create(self, class_name, *init_args):
        for module_obj in self._modules:
            try:
                class_obj = getattr(module_obj, class_name)
            except AttributeError:
                continue
            return class_obj(*init_args)
        raise AttributeError('Class ' + class_name + ' not found in module ' + self._module + ' - missing import?')

    def _get_modules(self):
        """
        Returns all modules which contains the given class
        """
        base = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', self._module))
        files = [f for f in listdir(base) if isfile(os.path.join(base, f)) and f.endswith('.py')]
        modules = []
        for file in files:
            try:
                file = file[:-3]
                modules.append(self._import('pollect.' + self._module + '.' + file))
            except ImportError as e:
                Log.warning('Could not import {}: {}'.format(file, str(e)))
                continue
        return modules

    @staticmethod
    def _import(package_name: str):
        return __import__(package_name, fromlist=[package_name])


class SourceFactory:
    def __init__(self, global_conf):
        self.global_conf = global_conf
        self._factory = ObjectFactory('sources')

    def create(self, source_data):
        source_type = source_data.get('type')
        class_name = source_type + 'Source'
        source_obj = self._factory.create(class_name, source_data)
        if not isinstance(source_obj, Source):
            raise TypeError('Class ' + class_name + ' does not inherit from "Source"')
        source_obj.setup(self.global_conf)
        return source_obj


class WriterFactory:
    """
    Factory for creating writer objects
    """

    def __init__(self, dry_run: bool = False):
        self._writer_cache = {}
        """
        Cache for writer singleton objects
        """
        self._factory = ObjectFactory('writers')
        self._dry_run = dry_run

    def create(self, writer_config):
        """
        Creates a new writer object from the given writer config.
        If a same writer with the same config does already exist, the same object will be returned

        :param writer_config: Writer configuration dict
        :type writer_config: dict(str, obj)
        :return: Writer object
        :rtype: Writer
        """
        class_name = writer_config.get('type') + 'Writer'
        if self._dry_run:
            return DryRunWriter(class_name)

        writer = self._factory.create(class_name, writer_config)
        if not isinstance(writer, Writer):
            raise TypeError('Class ' + class_name + ' does not inherit from "Writer"')
        old_writers = self._writer_cache.get(class_name)
        if old_writers is None:
            # New class type
            writer.start()
            self._writer_cache[class_name] = [writer]
            return writer

        for old_writer in old_writers:
            if old_writer == writer:
                # An old writer object has the same config - reuse it
                return old_writer

        # New writer - add it to the singleton cache
        writer.start()
        self._writer_cache[class_name].append(writer)
