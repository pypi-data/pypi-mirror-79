# Copyright 2017 Catalyst IT Limited
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import os
import shutil
import tempfile
import zipfile

from osc_lib.command import command
from osc_lib import utils
from oslo_utils import uuidutils

from qinlingclient.common import exceptions
from qinlingclient.osc.v1 import base
from qinlingclient import utils as q_utils

MAX_ZIP_SIZE = 50 * 1024 * 1024


def _get_package_file(package_path=None, file_path=None):
    if package_path:
        if not zipfile.is_zipfile(package_path):
            raise exceptions.QinlingClientException(
                'Package %s is not a valid ZIP file.' % package_path
            )

        if os.path.getsize(package_path) > MAX_ZIP_SIZE:
            raise exceptions.QinlingClientException(
                'Package file size must be no more than %sM.' %
                (MAX_ZIP_SIZE / 1024 / 1024)
            )

        return package_path

    elif file_path:
        if not os.path.isfile(file_path):
            raise exceptions.QinlingClientException(
                'File %s not exist.' % file_path
            )

        base_name, extension = os.path.splitext(file_path)
        base_name = os.path.basename(base_name)
        zip_file = os.path.join(
            tempfile.gettempdir(),
            '%s.zip' % base_name
        )

        zf = zipfile.ZipFile(zip_file, mode='w')
        try:
            # Use default compression mode, may change in future.
            zf.write(
                file_path,
                '%s%s' % (base_name, extension),
                compress_type=zipfile.ZIP_STORED
            )
        finally:
            zf.close()

        if os.path.getsize(zip_file) > MAX_ZIP_SIZE:
            raise exceptions.QinlingClientException(
                'Package file size must be no more than %sM.' %
                (MAX_ZIP_SIZE / 1024 / 1024)
            )

        return zip_file


def worker_count(value):
    try:
        value = int(value)
        if value <= 0:
            raise ValueError
    except ValueError:
        raise exceptions.QinlingClientException(
            'Worker count must be a positive integer.'
        )
    return value


class List(base.QinlingLister):
    columns = base.FUNCTION_COLUMNS
    filtered_columns = base.FILTERED_FUNCTION_COLUMNS

    def _get_resources(self, parsed_args):
        client = self.app.client_manager.function_engine

        return client.functions.list(**base.get_filters(parsed_args))


class Create(command.ShowOne):
    columns = base.FUNCTION_COLUMNS

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)

        parser.add_argument(
            "--runtime",
            help="Runtime ID. Runtime is needed for function of package type "
                 "and swift type, but not for the image type function.",
        )
        parser.add_argument(
            "--name",
            help="Function name.",
        )
        parser.add_argument(
            "--entry",
            help="Function entry in the format of <module_name>.<method_name>"
        )
        protected_group = parser.add_mutually_exclusive_group(required=False)
        protected_group.add_argument(
            "--file",
            metavar="CODE_FILE_PATH",
            help="Code file path."
        )
        protected_group.add_argument(
            "--package",
            metavar="CODE_PACKAGE_PATH",
            help="Code package zip file path."
        )
        parser.add_argument(
            "--container",
            help="Container name in Swift.",
        )
        parser.add_argument(
            "--object",
            help="Object name in Swift.",
        )
        parser.add_argument(
            "--image",
            help="Image name in docker hub.",
        )
        parser.add_argument(
            "--cpu",
            type=q_utils.check_positive,
            help="Limit of cpu resource(unit: millicpu).",
        )
        parser.add_argument(
            "--memory-size",
            type=q_utils.check_positive,
            help="Limit of memory resource(unit: bytes).",
        )
        parser.add_argument(
            "--timeout",
            type=q_utils.check_positive,
            default=5,
            help="The function execution time at which Qinling should "
                 "terminate the function. The default is 5 seconds",
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.function_engine
        code_type = None

        if (parsed_args.file or parsed_args.package):
            code_type = 'package'
        elif (parsed_args.container or parsed_args.object):
            code_type = 'swift'
        elif parsed_args.image:
            code_type = 'image'
        else:
            raise exceptions.QinlingClientException(
                'Cannot create function with the parameters given.\nMust '
                'provide required parameters for different type of '
                'functions:\n'
                '    - for package type function, either --file or --package '
                'is required,\n'
                '    - for swift type function, both --container and --object '
                'are required,\n'
                '    - for image type function, --image is required.'
            )

        runtime = parsed_args.runtime
        if runtime and not uuidutils.is_uuid_like(runtime):
            # Try to find the runtime id with name
            runtime = q_utils.find_resource_id_by_name(
                client.runtimes, runtime)

        if code_type == 'package':
            if not runtime:
                raise exceptions.QinlingClientException(
                    'Runtime needs to be specified for package type function.'
                )

            zip_file = _get_package_file(parsed_args.package, parsed_args.file)
            md5sum = q_utils.md5(file=zip_file)
            code = {"source": "package", "md5sum": md5sum}

            with open(zip_file, 'rb') as package:
                function = client.functions.create(
                    name=parsed_args.name,
                    runtime=runtime,
                    code=code,
                    package=package,
                    entry=parsed_args.entry,
                    cpu=parsed_args.cpu,
                    memory_size=parsed_args.memory_size,
                    timeout=parsed_args.timeout
                )

            # Delete zip file the client created
            if parsed_args.file and not parsed_args.package:
                os.remove(zip_file)

        elif code_type == 'swift':
            if not (parsed_args.container and parsed_args.object):
                raise exceptions.QinlingClientException(
                    'Container name and object name need to be specified.'
                )
            if not runtime:
                raise exceptions.QinlingClientException(
                    'Runtime needs to be specified for swift type function.'
                )

            code = {
                "source": "swift",
                "swift": {
                    "container": parsed_args.container,
                    "object": parsed_args.object
                }
            }

            function = client.functions.create(
                name=parsed_args.name,
                runtime=runtime,
                code=code,
                entry=parsed_args.entry,
                cpu=parsed_args.cpu,
                memory_size=parsed_args.memory_size,
                timeout=parsed_args.timeout
            )

        elif code_type == 'image':
            code = {
                "source": "image",
                "image": parsed_args.image
            }

            function = client.functions.create(
                name=parsed_args.name,
                code=code,
                entry=parsed_args.entry,
                cpu=parsed_args.cpu,
                memory_size=parsed_args.memory_size,
                timeout=parsed_args.timeout
            )

        return self.columns, utils.get_item_properties(function, self.columns)


class Delete(base.QinlingDeleter):
    def get_parser(self, prog_name):
        parser = super(Delete, self).get_parser(prog_name)

        parser.add_argument(
            'function',
            nargs='+',
            metavar='FUNCTION',
            help='Id or name of function(s).'
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.function_engine
        self.delete = client.functions.delete
        self.resource = 'function'

        ids = []
        for function_id in parsed_args.function:
            if not uuidutils.is_uuid_like(function_id):
                function_id = q_utils.find_resource_id_by_name(
                    client.functions, function_id)
            ids.append(function_id)

        self.delete_resources(ids)


class Show(command.ShowOne):
    columns = base.FUNCTION_COLUMNS

    def get_parser(self, prog_name):
        parser = super(Show, self).get_parser(prog_name)
        parser.add_argument('function', help='Function ID or name.')

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.function_engine

        function_id = parsed_args.function
        if not uuidutils.is_uuid_like(function_id):
            function_id = q_utils.find_resource_id_by_name(
                client.functions, function_id)

        function = client.functions.get(function_id)
        return self.columns, utils.get_item_properties(function,
                                                       self.columns)


class Update(command.ShowOne):
    columns = base.FUNCTION_COLUMNS

    def get_parser(self, prog_name):
        parser = super(Update, self).get_parser(prog_name)

        parser.add_argument(
            'function',
            help='Function ID or name.'
        )
        parser.add_argument(
            "--name",
            help="Function name."
        )
        parser.add_argument(
            "--description",
            help="Function description."
        )
        parser.add_argument(
            "--entry",
            help="Function entry in the format of <module_name>.<method_name>"
        )

        package_group = parser.add_mutually_exclusive_group()
        package_group.add_argument(
            "--file",
            metavar="CODE_FILE_PATH",
            help="Code file path."
        )
        package_group.add_argument(
            "--package",
            metavar="CODE_PACKAGE_PATH",
            help="Code package zip file path."
        )

        # For swift functions
        parser.add_argument(
            "--container",
            help="Container name in Swift.",
        )
        parser.add_argument(
            "--object",
            help="Object name in Swift.",
        )

        parser.add_argument(
            "--cpu",
            type=q_utils.check_positive,
            help="Limit of cpu resource(unit: millicpu).",
        )
        parser.add_argument(
            "--memory-size",
            type=q_utils.check_positive,
            help="Limit of memory resource(unit: bytes).",
        )
        parser.add_argument(
            "--timeout",
            type=q_utils.check_positive,
            help="The function execution time at which Qinling should "
                 "terminate the function. The default is 5 seconds",
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.function_engine
        code = None
        package = None
        zip_file = None

        function_id = parsed_args.function
        if not uuidutils.is_uuid_like(function_id):
            function_id = q_utils.find_resource_id_by_name(
                client.functions, function_id)

        if parsed_args.file or parsed_args.package:
            code = {'source': 'package'}
            zip_file = _get_package_file(parsed_args.package, parsed_args.file)
        elif parsed_args.container or parsed_args.object:
            swift = {}
            if parsed_args.container:
                swift["container"] = parsed_args.container
            if parsed_args.object:
                swift["object"] = parsed_args.object
            code = {'source': 'swift', 'swift': swift}

        if zip_file:
            with open(zip_file, 'rb') as package:
                func = client.functions.update(
                    function_id,
                    code=code,
                    package=package,
                    name=parsed_args.name,
                    description=parsed_args.description,
                    entry=parsed_args.entry,
                    cpu=parsed_args.cpu,
                    memory_size=parsed_args.memory_size,
                    timeout=parsed_args.timeout
                )
        else:
            func = client.functions.update(
                function_id,
                code=code,
                name=parsed_args.name,
                description=parsed_args.description,
                entry=parsed_args.entry,
                cpu=parsed_args.cpu,
                memory_size=parsed_args.memory_size,
                timeout=parsed_args.timeout
            )

        return self.columns, utils.get_item_properties(func, self.columns)


class Detach(command.Command):
    def get_parser(self, prog_name):
        parser = super(Detach, self).get_parser(prog_name)
        parser.add_argument('function', help='Function ID.')

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.function_engine
        success_msg = "Request to detach function %s has been accepted."
        error_msg = "Unable to detach the specified function."

        try:
            client.functions.detach(parsed_args.function)
            print(success_msg % parsed_args.function)
        except Exception as e:
            print(e)
            raise exceptions.QinlingClientException(error_msg)


class Download(command.Command):
    def get_parser(self, prog_name):
        parser = super(Download, self).get_parser(prog_name)
        parser.add_argument('function', help='Function ID or name.')
        parser.add_argument(
            "-o",
            "--output",
            help="Target file path. If not provided, function ID will be used"
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.function_engine

        function_id = parsed_args.function
        if not uuidutils.is_uuid_like(function_id):
            function_id = q_utils.find_resource_id_by_name(
                client.functions, function_id)

        res = client.functions.get(function_id, download=True)

        cwd = os.getcwd()
        if parsed_args.output:
            if os.path.isabs(parsed_args.output):
                abs_path = parsed_args.output
            else:
                abs_path = os.path.join(cwd, parsed_args.output)
        else:
            abs_path = os.path.join(cwd, "%s.zip" % function_id)

        with open(abs_path, 'wb') as target:
            shutil.copyfileobj(res.raw, target)
        print("Code package downloaded to %s" % (abs_path))


class Scaleup(command.Command):
    def get_parser(self, prog_name):
        parser = super(Scaleup, self).get_parser(prog_name)
        parser.add_argument('function', help='Function ID.')
        parser.add_argument('--count', type=worker_count, default=1,
                            help='Number of workers to scale up.')

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.function_engine
        success_msg = "Request to scale up function %s has been accepted."
        error_msg = "Unable to scale up the specified function."

        try:
            client.functions.scaleup(parsed_args.function, parsed_args.count)
            print(success_msg % parsed_args.function)
        except Exception as e:
            print(e)
            raise exceptions.QinlingClientException(error_msg)


class Scaledown(command.Command):
    def get_parser(self, prog_name):
        parser = super(Scaledown, self).get_parser(prog_name)
        parser.add_argument('function', help='Function ID.')
        parser.add_argument('--count', type=worker_count, default=1,
                            help='Number of workers to scale down.')

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.function_engine
        success_msg = "Request to scale down function %s has been accepted."
        error_msg = "Unable to scale down the specified function."

        try:
            client.functions.scaledown(parsed_args.function, parsed_args.count)
            print(success_msg % parsed_args.function)
        except Exception as e:
            print(e)
            raise exceptions.QinlingClientException(error_msg)
