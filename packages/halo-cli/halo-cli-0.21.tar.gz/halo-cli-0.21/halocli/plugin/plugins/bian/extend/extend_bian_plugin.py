from __future__ import print_function
import sys
import os
import logging
import json
import copy
from os.path import dirname
from jsonschema import validate
import importlib
import pkgutil
import tempfile
import uuid
from halocli.exception import HaloPluginException
from halocli.util import Util

logger = logging.getLogger(__name__)

logging.root.setLevel(logging.INFO)

"""
the bian plugin
---------------

1. no segregation and add id for no segregation items - done

2. add proprietary bank fields from legacy - done

3. add mappings from legacy to bian fields

4. generate collection-filter parameter list

5. add sub BQ as needed

6. add new endpoints as needed

7. refactor bian types in specific fields where type is generic(string, etc..)

8. add version metadata for control and traceability

"""

class Plugin():

    def __init__(self,halo):
        #init vars
        self.halo = halo

        #init work on halo config
        #if self.halo.config ...

        self.name = 'extend'
        self.desc = 'extend bian swagger file'

        # set commands
        self.commands = {
            'all': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
            'fields': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
            'mappings': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
            'filter': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
            'refactor': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
            'headers': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
            'errors': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's'
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    }
                },
            },
        }

        # set hooks
        self.hooks = {
            'before:fields:generate': self.before_fields_generate,
            'fields:generate': self.fields_generate,
            'after:fields:generate': self.after_fields_generate,
            'fields:write': self.fields_write,
            'before:refactor:generate': self.before_refactor_generate,
            'refactor:generate': self.refactor_generate,
            'after:refactor:generate': self.after_refactor_generate,
            'refactor:write': self.refactor_write,
        }

        #logger.info('finished plugin')

    def run_plugin(self,options):
        self.options = options
        #do more
        self.before()

    def before(self):
        service = None
        path = None
        if hasattr(self, 'options'):
            if self.options:
                for o in self.options:
                    if 'service' in o:
                        service = o['service']
                    if 'path' in o:
                        path = o['path']
        if not service:
            raise Exception("no service found")
        self.service = service
        urls = self.halo.settings['mservices'][service]['record']['path']
        self.path = path
        self.data = Util.analyze_swagger(urls)

    def before_fields_generate(self):
        if "company" in self.halo.settings['mservices'][self.service]['record']:
            self.data["info"]["title"] = self.halo.settings['mservices'][self.service]['record']['company']+ " - " + self.data["info"]["title"]



    def fields_generate(self):
        data = self.data
        tmp = {}
        for d in data['paths']:
            m = data['paths'][d]
            if 'get' in m:
                if 'ReferenceIdsExtend' in m['get']['operationId']:
                    new_m = copy.deepcopy(m)
                    tmp[d] = new_m
        # fix the response and add
        for k in tmp:
            # bq methods
            ref_m = tmp[k]
            new_m = copy.deepcopy(ref_m)
            props = new_m['get']['responses']['200']['schema']['items']['properties']
            for p in props:
                if "methods" in self.halo.settings['mservices'][self.service]['record']:
                    for mthd in self.halo.settings['mservices'][self.service]['record']['methods']:
                        if mthd == new_m['get']['operationId']:
                            for target in self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['added_fields']:
                                if p.endswith(target):
                                    self.halo.cli.log(new_m['get']['operationId'])
                                    #props[p]['properties']["ObjectReference"] = {"type":"string"}
                                    for fld in self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['added_fields'][target]:
                                        type = self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['added_fields'][target][fld]
                                        props[p]['properties'][fld] = {"type": type}
            data['paths'][k] = new_m

    def after_fields_generate(self):
        data = self.data
        Util.validate_swagger(data)

    def fields_write(self):
        self.file_write()

    def file_write(self):
        try:
            path = self.path
            if path:
                file_path = os.path.join(path, str(uuid.uuid4()) + ".json")
            else:
                dir_tmp = tempfile.TemporaryDirectory()
                file_path = os.path.join(dir_tmp.name, str(uuid.uuid4()) + ".json")
            logger.debug(file_path)
            f = open(file_path, "a")
            f.write("")
            f.close()
            Util.dump_file(file_path, self.data)
            logging.debug("Swagger file generated:" + file_path)
            """
            with open(file_path, 'r') as fi:
                f = fi.read()
                print(str(f))
                return f
            """
            return 0
        except Exception as e:
            raise HaloPluginException(str(e))


    def before_refactor_generate(self):
        self.before()

    def refactor_generate(self):
        data = self.data
        tmp = {}
        for d in data['paths']:
            m = data['paths'][d]
            if 'get' in m:
                if 'ReferenceIdsExtend' in m['get']['operationId']:
                    new_m = copy.deepcopy(m)
                    tmp[d] = new_m
        # fix the response and add
        for k in tmp:
            # bq methods
            ref_m = tmp[k]
            new_m = copy.deepcopy(ref_m)
            props = new_m['get']['responses']['200']['schema']['items']['properties']
            for p in props:
                if "methods" in self.halo.settings['mservices'][self.service]['record']:
                    for mthd in self.halo.settings['mservices'][self.service]['record']['methods']:
                        if mthd == new_m['get']['operationId']:
                            for target in self.halo.settings['mservices'][self.service]['record']['methods'][mthd]['refactor']:
                                fields = target['field'].split(".")
                                if p.endswith(fields[0]):
                                    #self.halo.cli.log(new_m['get']['operationId']+":"+p)
                                    size = len(fields)
                                    i = 1
                                    props = props[p]
                                    while i < size:
                                        name = fields[i]
                                        props = props['properties'][name]
                                        i = i + 1
                                    type = target['type']
                                    props['type'] = type
            data['paths'][k] = new_m

    def after_refactor_generate(self):
        pass

    def refactor_write(self):
        self.file_write()