__version__ = "0.2.0"

from .artefacts import File, Directory
from .manager import Manager
from .utils import find, connect

from .stateless import (
    artefact,
    exists,
    isabs,
    abspath,
    relpath,
    commonprefix,
    commonpath,
    basename,
    dirname,
    join,
    touch,
    mkdir,
    localise,
    open,
    get,
    put,
    ls,
    cp,
    mv,
    sync,
    rm
)