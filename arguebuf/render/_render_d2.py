import os
from tempfile import NamedTemporaryFile
import typing as t
from pathlib import Path
from subprocess import run
from arguebuf.schemas.d2 import D2Graph

__all__ = ("d2",)
FORMATS = ["png", "pdf", "svg"]


def d2(
        graph: D2Graph,
        dir: t.Union[Path, str] = "",
        format: str = "svg",
        filename: str = "graph",
) -> None:
    """Visualize a Graph instance using a D2 backend. Make sure that a D2 Executable path is set on your machine for visualization."""

    if format not in FORMATS:
        raise ValueError(
            "You need to provide a path with a file ending supported by d2:"
            f" {FORMATS}"
        )

    if isinstance(dir, str):
        dir = Path(dir)

    # Create temporary file
    tmp = NamedTemporaryFile(delete=False, mode="w")
    try:
        tmp.write(str(graph))
    finally:
        tmp.close()
        # run d2 command and produce the output file
        path = os.path.join(str(dir), filename + "." + format)
        run(["d2", tmp.name, path])
        # remove temporary file
        os.unlink(tmp.name)
