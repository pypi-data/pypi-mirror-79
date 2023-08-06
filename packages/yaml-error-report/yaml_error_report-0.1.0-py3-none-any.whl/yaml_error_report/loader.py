from .types import AnyPath, JsonPath
from typing import Any, Mapping, Union, IO
import yaml
from yaml.loader import SafeLoader
import wrapt

from .types import Location


class NodeWithLoc(wrapt.ObjectProxy):
    """Constructed YAML node wrapped with location metadata"""
    def __init__(self, wrapped, location: Location):
        super().__init__(wrapped)
        self._self_wrapped = wrapped
        self._self_loc = location

    @property
    def location(self) -> Location:
        """The text location of this object within the source file"""
        return self._self_loc

    def __str__(self):
        return str(self._self_wrapped)

    def __repr__(self):
        return f"<{self._self_wrapped!r} @ {self._self_loc!r}>"


def make_loader(filename: str) -> SafeLoader:
    """Create a loader which knows the filename its loading"""
    class SafeLineLoader(SafeLoader):
        def make_loc(self, node):
            return Location(
                node.start_mark.line + 1,
                node.start_mark.column,
                node.end_mark.line + 1,
                node.end_mark.column,
                node.start_mark.index,
                node.end_mark.index,
                filename
            )

        def construct_object(self, node, deep=False):
            res = super().construct_object(node, deep=deep)
            # wrap the node with in proxy object which knows its text source location
            return NodeWithLoc(res, self.make_loc(node))

    return SafeLineLoader


def load_stream(stream: Union[bytes, IO[bytes], str, IO[str]], filename: AnyPath) -> NodeWithLoc:
    """Load a yaml from a stream and return the annotated object"""
    return yaml.load(stream, Loader=make_loader(str(filename)))


def load_file(filename: AnyPath) -> NodeWithLoc:
    """Load a yaml file and return the annotated object"""
    with open(filename, "r") as f:
        return load_stream(f, filename)


def path_to_location(filename: AnyPath, path: JsonPath) -> Location:
    """Convert a json object path into a text location

    Args:
        filename: The yaml/json source file path
        path: The path to the object within the file expressed as a sequence of keys

    Returns: The text location of object within the file
    """
    data = load_file(filename)
    node = apply_path(data, path)
    return node.location


def apply_path(data: Mapping[str, Any], path: JsonPath) -> Any:
    """Apply a jsonpath to the json-like dict and get the target node"""
    node = data
    for e in path:
        node = node[e]
    return node
