# Copyright 2020 The gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

_REQUIRED_SYMBOLS = ("_protos", "_services", "_protos_and_services")


def _uninstalled_protos(*args, **kwargs):
    raise NotImplementedError(
        "Install the grpcio-tools package (1.32.0+) to use the protos function."
    )


def _uninstalled_services(*args, **kwargs):
    raise NotImplementedError(
        "Install the grpcio-tools package (1.32.0+) to use the services function."
    )


def _uninstalled_protos_and_services(*args, **kwargs):
    raise NotImplementedError(
        "Install the grpcio-tools package (1.32.0+) to use the protos_and_services function."
    )


def _interpreter_version_protos(*args, **kwargs):
    raise NotImplementedError(
        "The protos function is only on available on Python 3.X interpreters.")


def _interpreter_version_services(*args, **kwargs):
    raise NotImplementedError(
        "The services function is only on available on Python 3.X interpreters."
    )


def _interpreter_version_protos_and_services(*args, **kwargs):
    raise NotImplementedError(
        "The protos_and_services function is only on available on Python 3.X interpreters."
    )


def protos(protobuf_path):  # pylint: disable=unused-argument
    """Returns a module generated by the indicated .proto file.

    THIS IS AN EXPERIMENTAL API.

    Use this function to retrieve classes corresponding to message
    definitions in the .proto file.

    To inspect the contents of the returned module, use the dir function.
    For example:

    ```
    protos = grpc.protos("foo.proto")
    print(dir(protos))
    ```

    The returned module object corresponds to the _pb2.py file generated
    by protoc. The path is expected to be relative to an entry on sys.path
    and all transitive dependencies of the file should also be resolveable
    from an entry on sys.path.

    To completely disable the machinery behind this function, set the
    GRPC_PYTHON_DISABLE_DYNAMIC_STUBS environment variable to "true".

    Args:
      protobuf_path: The path to the .proto file on the filesystem. This path
        must be resolveable from an entry on sys.path and so must all of its
        transitive dependencies.

    Returns:
      A module object corresponding to the message code for the indicated
      .proto file. Equivalent to a generated _pb2.py file.
    """


def services(protobuf_path):  # pylint: disable=unused-argument
    """Returns a module generated by the indicated .proto file.

    THIS IS AN EXPERIMENTAL API.

    Use this function to retrieve classes and functions corresponding to
    service definitions in the .proto file, including both stub and servicer
    definitions.

    To inspect the contents of the returned module, use the dir function.
    For example:

    ```
    services = grpc.services("foo.proto")
    print(dir(services))
    ```

    The returned module object corresponds to the _pb2_grpc.py file generated
    by protoc. The path is expected to be relative to an entry on sys.path
    and all transitive dependencies of the file should also be resolveable
    from an entry on sys.path.

    To completely disable the machinery behind this function, set the
    GRPC_PYTHON_DISABLE_DYNAMIC_STUBS environment variable to "true".

    Args:
      protobuf_path: The path to the .proto file on the filesystem. This path
        must be resolveable from an entry on sys.path and so must all of its
        transitive dependencies.

    Returns:
      A module object corresponding to the stub/service code for the indicated
      .proto file. Equivalent to a generated _pb2_grpc.py file.
    """


def protos_and_services(protobuf_path):  # pylint: disable=unused-argument
    """Returns a 2-tuple of modules corresponding to protos and services.

    THIS IS AN EXPERIMENTAL API.

    The return value of this function is equivalent to a call to protos and a
    call to services.

    To completely disable the machinery behind this function, set the
    GRPC_PYTHON_DISABLE_DYNAMIC_STUBS environment variable to "true".

    Args:
      protobuf_path: The path to the .proto file on the filesystem. This path
        must be resolveable from an entry on sys.path and so must all of its
        transitive dependencies.

    Returns:
      A 2-tuple of module objects corresponding to (protos(path), services(path)).
    """


if sys.version_info < (3, 5, 0):
    protos = _interpreter_version_protos
    services = _interpreter_version_services
    protos_and_services = _interpreter_version_protos_and_services
else:
    try:
        import grpc_tools  # pylint: disable=unused-import
    except ImportError as e:
        # NOTE: It's possible that we're encountering a transitive ImportError, so
        # we check for that and re-raise if so.
        if "grpc_tools" not in e.args[0]:
            raise
        protos = _uninstalled_protos
        services = _uninstalled_services
        protos_and_services = _uninstalled_protos_and_services
    else:
        import grpc_tools.protoc  # pylint: disable=unused-import
        if all(hasattr(grpc_tools.protoc, sym) for sym in _REQUIRED_SYMBOLS):
            from grpc_tools.protoc import _protos as protos  # pylint: disable=unused-import
            from grpc_tools.protoc import _services as services  # pylint: disable=unused-import
            from grpc_tools.protoc import _protos_and_services as protos_and_services  # pylint: disable=unused-import
        else:
            protos = _uninstalled_protos
            services = _uninstalled_services
            protos_and_services = _uninstalled_protos_and_services
