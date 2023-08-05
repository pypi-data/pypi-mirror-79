#!/usr/bin/env python3
# vim: set filetype=python sts=4 ts=4 sw=4 expandtab tw=100 cc=+1:
# vim: set filetype=python tw=100 cc=+1:
# pylint: disable=reimported,wrong-import-position
# pylint: disable=missing-docstring
# pylint: disable=bad-option-value,bad-continuation
# pylint: disable=ungrouped-imports
# pylint: disable=dangerous-default-value

# mypy: warn-unused-configs, disallow-any-generics, disallow-subclassing-any
# mypy: disallow-untyped-calls, disallow-untyped-defs, disallow-incomplete-defs
# mypy: check-untyped-defs, disallow-untyped-decorators, no-implicit-optional,
# mypy: warn-redundant-casts, warn-unused-ignores, warn-return-any, no-implicit-reexport,
# mypy: strict-equality

"""
This module is boilerplate for a python CLI script.
"""

# python3 -m pylint --rcfile=/dev/null boilerplate.py
# python3 -m mypy boilerplate.py

import logging
LOGGER = logging.getLogger(__name__)

import os.path
SCRIPT_DIRNAME = os.path.dirname(__file__)
SCRIPT_DIRNAMEABS = os.path.abspath(SCRIPT_DIRNAME)
SCRIPT_BASENAME = os.path.basename(__file__)

import pathlib
SCRIPT_PATH = pathlib.Path(__file__)

import sys
import argparse
import contextlib
import typing as typ
import inspect
import yaml
import pyld
from pyld import jsonld
import json
import enum

from . import __version__

GenericT = typ.TypeVar('GenericT')
def collate(*args: typ.Optional[GenericT]) -> typ.Optional[GenericT]:
    for arg in args:
        if arg is not None:
            return arg
    return None

def vdict(*keys: str, obj: typ.Any = None) -> typ.Dict[str, typ.Any]:
    if obj is None:
        lvars = typ.cast(typ.Any, inspect.currentframe()).f_back.f_locals
        return {key: lvars[key] for key in keys}
    return {key: getattr(obj, key, None) for key in keys}

class Format(enum.Enum):
    JSON = enum.auto()
    YAML = enum.auto()
    NQUADS = enum.auto()

ArgsT = typ.List[str]
OptArgsT = typ.Optional[ArgsT]
OptParseResultT = typ.Optional[argparse.Namespace]
OptParserT = typ.Optional[argparse.ArgumentParser]
class Application:
    parser: argparse.ArgumentParser
    args: OptArgsT
    parse_result: OptParseResultT
    def __init__(self, parser: OptParserT = None):
        LOGGER.debug("entry ...")
        self.parse_result = None
        self.args = None
        self._do_init(parser)

    def _do_init(self, parser: OptParserT = None) -> None:
        LOGGER.debug("entry ...")
        if parser is None:
            own_parser = True
            self.parser = argparse.ArgumentParser(add_help=True)
        else:
            self.parser = parser
            own_parser = False
        parser = self.parser
        if own_parser:
            parser.add_argument("-v", "--verbose", action="count", dest="verbosity",
                help="increase verbosity level")
        parser.add_argument("--version", "-V", action="version",
            version=("%(prog)s " + __version__))
        parser.set_defaults(handler=self.handle)
        parsers: typ.List[argparse.ArgumentParser] = [parser]

        @contextlib.contextmanager
        def new_subparser(name: str, parser_args: typ.Dict[str, typ.Any] = {},
            subparsers_args: typ.Dict[str, typ.Any] = {}) \
            -> typ.Generator[argparse.ArgumentParser, None, None]:
            parent_parser = parsers[-1]
            if not hasattr(parent_parser, '_xsubparsers'):
                setattr(parent_parser, '_xsubparsers',
                    parent_parser.add_subparsers(dest=f"subparser_{len(parsers)}",
                        **subparsers_args))
            parent_subparsers = getattr(parent_parser, '_xsubparsers')
            parsers.append(parent_subparsers.add_parser(name, **parser_args))
            try:
                yield parsers[-1]
            finally:
                parsers.pop()

        def common_options(subparser: argparse.ArgumentParser,
            extra: typ.Set[str] = set()) -> None:
            subparser.add_argument("--url-handling", "--url", "-U",
                action="store_true", default=False,
                help="Defers input handling to backend which may support URLs")
            subparser.add_argument("--input-format", "--if", "-I",
                action="store", type=str, default="YAML",
                help="Format to use for input, must be NQUADS, YAML or JSON")
            subparser.add_argument("--output-format", "--of", "-O",
                action="store", type=str, default="JSON",
                help="Format to use for output, must be NQUADS, YAML or JSON")
            subparser.add_argument("input",
                action="append", nargs="?",
                help="Input file, - for stdin")
            subparser.add_argument("--output", "-o",
                action="store", type=str, default="-",
                help="Output file, - for stdout")
            subparser.add_argument("--inject-context", "-o",
                action="store", type=str, default="-",
                help="...")
            subparser.add_argument("--base",
                action="store", type=str, required=False,
                help="Base IRI.")
            if "context" in extra:
                subparser.add_argument("--context-file", "--context", "--cf", "-c",
                    action="store", type=str, required=False,
                    help="Context to when compacting.")
            if "expand-context" in extra:
                subparser.add_argument("--expand-context",
                    action="store", type=str, required=False,
                    help="A context to expand with.")
            if "processing-mode" in extra:
                subparser.add_argument("--processing-mode",
                    action="store", type=str, required=False, default="json-ld-1.1",
                    help="Either 'json-ld-1.0' or 'json-ld-1.1'.")

        with new_subparser("compact") as subparser:
            subparser.set_defaults(handler=self.handle_api)
            common_options(subparser, set(["context", "expand-context", "processing-mode"]))
            subparser.add_argument("--compact-arrays",
                action="store", type=bool, default=False,
                help=("True to compact arrays to single values "
                    "when appropriate, False not to."))
            subparser.add_argument("--graph",
                action="store", type=bool, default=False,
                help=("True to always output a top-level graph."))

        with new_subparser("cat") as subparser:
            subparser.set_defaults(handler=self.handle_api)
            common_options(subparser, set([]))
        with new_subparser("expand") as subparser:
            subparser.set_defaults(handler=self.handle_api)
            common_options(subparser, set(["context", "expand-context", "processing-mode"]))
            subparser.add_argument("--is-frame",
                action="store", type=bool, default=False,
                help=("True to allow framing keywords and interpretation, False not to."))
            subparser.add_argument("--keep-free-floating-nodes",
                action="store", type=bool, default=False,
                help=("True to always output a top-level graph."))
        with new_subparser("flatten") as subparser:
            subparser.set_defaults(handler=self.handle_api)
            common_options(subparser, set(["context", "expand-context", "processing-mode"]))
        with new_subparser("frame") as subparser:
            subparser.set_defaults(handler=self.handle_api)
            common_options(subparser, set(["context", "expand-context", "processing-mode"]))
            subparser.add_argument("--embed",
                action="store", type=str, default="@last",
                help="default @embed flag: '@last', '@always', '@never', '@link'.")
            subparser.add_argument("--explicit",
                action="store", type=bool, default=False,
                help="default @explicit flag")
            # TODO: add other options ...
        with new_subparser("normalize") as subparser:
            subparser.set_defaults(handler=self.handle_api)
            common_options(subparser, set([]))


    def _parse_args(self, args: OptArgsT = None) -> None:
        LOGGER.debug("entry ...")
        self.args = collate(args, self.args, sys.argv[1:])
        self.parse_result = self.parser.parse_args(self.args)

        verbosity = self.parse_result.verbosity
        if verbosity is not None:
            root_logger = logging.getLogger("")
            root_logger.propagate = True
            new_level = (root_logger.getEffectiveLevel() -
                (min(1, verbosity)) * 10 - min(max(0, verbosity - 1), 9) * 1)
            root_logger.setLevel(new_level)

        LOGGER.debug("args = %s, parse_result = %s, logging.level = %s, LOGGER.level = %s",
            self.args, self.parse_result, logging.getLogger("").getEffectiveLevel(),
            LOGGER.getEffectiveLevel())

        if "handler" in self.parse_result and self.parse_result.handler:
            self.parse_result.handler(self.parse_result)

    def do_invoke(self, args: OptArgsT = None) -> None:
        self._parse_args(args)

    # parser is so this can be nested as a subcommand ...
    @classmethod
    def invoke(cls, *, parser: OptParserT = None, args: OptArgsT = None) -> None:
        app = cls(parser)
        app.do_invoke(args)

    def handle(self, parse_result: OptParseResultT = None) -> None:
        LOGGER.debug("entry ...")
        self.parse_result = parse_result = collate(parse_result, self.parse_result)

    def handle_api(self, parse_result: OptParseResultT = None) -> None:
        LOGGER.debug("entry ...")
        self.handle(parse_result)
        parse_result = self.parse_result
        assert parse_result
        command = parse_result.subparser_1

        input_format = Format[parse_result.input_format]
        output_format = Format[parse_result.output_format]
        def read_input_fileh(fileh: typ.TextIO) -> typ.Any:
            if input_format is Format.JSON:
                return json.load(fileh)
            elif input_format is Format.YAML:
                return yaml.safe_load(fileh)
            elif input_format is Format.NQUADS:
                return jsonld.from_rdf(fileh)

        def read_input_file(input_spec: str,
            fileh: typ.Optional[typ.TextIO] = None) -> typ.Any:
            if fileh:
                return read_input_fileh(fileh)
            else:
                input_path = pathlib.Path(input_spec)
                with input_path.open("r") as fileh:
                    return read_input_fileh(fileh)

        def read_input_spec(input_spec: str) -> typ.Any:
            if input_spec == "-":
                return read_input_file("-", sys.stdin)
            else:
                return read_input_file(input_spec)

        context_spec = getattr(parse_result, 'context_file', None)
        frame_spec = getattr(parse_result, 'frame_file', None)
        inject_context_spec = getattr(parse_result, 'inject_context', None)
        input_spec = parse_result.input[0]
        output_spec = parse_result.output
        LOGGER.debug(vdict('input_spec', 'context_spec', 'output_spec', 'frame_spec'))

        url_handling = parse_result.url_handling
        if url_handling:
            input_param = input_spec
            context_param = context_spec
            frame_param = frame_spec
            inject_context_param = inject_context_spec
        else:
            input_param = read_input_spec(input_spec)
            context_param = read_input_spec(context_spec) \
                if context_spec else None
            frame_param = read_input_spec(frame_spec) \
                if frame_spec else None
            if inject_context_spec:
                inject_context = read_input_spec(inject_context_spec)
                input_param.update(inject_context)

        LOGGER.debug(vdict('input_param', 'context_param'))

        options_map = {
            "base": "base",
            "compactArrays": "compact-arrays",
            "graph": "graph",
            "expandContext": "expand-context",
            "isFrame": "is-frame",
            "keepFreeFloatingNodes": "keep-free-floating-nodes",
            "processingMode": "processing-mode",
            "embed": "embed",
            "explicit": "explicit",
        }

        options = {}
        for okey, ovalue in options_map.items():
            if hasattr(parse_result, ovalue):
                options[okey] = getattr(parse_result, ovalue)


        LOGGER.debug(vdict('options'))
        result = {}
        if command == "compact":
            result = jsonld.compact(input_param, context_param or {}, options=options)
        elif command == "expand":
            result = jsonld.expand(input_param, options=options)
        elif command == "flatten":
            result = jsonld.flatten(input_param, context_param or {}, options=options)
        elif command == "frame":
            result = jsonld.frame(input_param, frame_param, options=options)
        elif command == "normalize":
            result = jsonld.normalize(input_param, options=options)
        elif command == "cat":
            result = input_param
        LOGGER.debug(vdict('result'))
        def write_output_fileh(data: typ.Any, fileh: typ.TextIO) -> None:
            if output_format is Format.JSON:
                json.dump(data, fileh, indent=2)
                fileh.write("\n")
            elif output_format is Format.YAML:
                yaml.safe_dump(data, fileh)
            elif output_format is Format.NQUADS:
                rdf = jsonld.to_rdf(data, {"format": "application/n-quads"})
                LOGGER.debug(vdict('data', 'rdf'))
                fileh.write(jsonld.to_rdf(data, {"format": "application/n-quads"}))

        def write_output_file(data: typ.Any, output_spec: str,
            fileh: typ.Optional[typ.TextIO] = None) -> None:
            if fileh:
                return write_output_fileh(data, fileh)
            else:
                input_path = pathlib.Path(output_spec)
                with open(input_path, "w") as fileh:
                    return write_output_fileh(data, fileh)

        def write_output_spec(data: typ.Any, output_spec: str) -> None:
            if output_spec == "-":
                return write_output_file(data, "-", sys.stdout)
            else:
                return write_output_file(data, output_spec)

        write_output_spec(result, parse_result.output)


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
        datefmt="%Y-%m-%dT%H:%M:%S",
        format=("%(asctime)s %(process)d %(thread)d %(levelno)03d:%(levelname)-8s "
            "%(name)-12s %(module)s:%(lineno)s:%(funcName)s %(message)s"))

    Application.invoke()

if __name__ == "__main__":
    main()
