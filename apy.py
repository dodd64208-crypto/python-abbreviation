# mini_py.py
import sys, importlib.abc, importlib.util, tokenize
from io import BytesIO

RULES = {
    "imp": "import",
    "impw": "ImportWarning",
    "dew": "DeprecationWarning",
    "zeder": "ZeroDivisionError",
    "ucder": "UnicodeDecodeError",
    "pdw": "PendingDeprecationWarning",
    "bytw": "BytesWarning",
    "userw": "UserWarning",
    "futw": "FutureWarning",
    "synw": "SyntaxWarning",
    "encnw": "EncodingWarning",
    "rtw": "RuntimeWarning",
    "synw": "SyntaxWarning",
    "resw": "ResourceWarning",
    "warn": "Warning",
    "winer": "WindowsError",
    "enver": "EnvironmentError",
    "kyer": "KeyError",
    "inder": "IndexError",
    "taber": "TabError",
    "nmer": "NameError",
    "typer": "TypeError",
    "enumt": "enumerate",
    "valer": "ValueError",
    "bufer": "BufferError",
    "eofer": "OSError",
    "lkuper": "LookupError",
    "memer": "MemoryError",
    "synter": "SyntaxError,
    "syser": "SystemError",
    "ruter": "RuntimeError",
    "timouter": "TimeoutError",
    "ucer": "UnicodeError",
    "ovfler": "OverflowError",
    "asseter": "AssertionError",
    "attber": "AttributeError",
    "envmeter": "EnvironmentError",
    "recurer": "RecursionError",
    "refener": "ReferenceError",
    "ariter": "ArithmeticError",
    "brkpipeer": "BrokenPipeError",
    "coner": "ConnectionError",
    "filexier": "FileExistsError",
    "prmer": "PermissionError",
    "modlntfder": "ModuleNotFoundError",
    "indenter": "IndentationError",
    "intuper": "InterruptedError",
    "ndter": "NotADirectoryError",
    "ntimemted": "NotImplemented",
    "ntimemteder": "NotImplementedError",
    "filentfer": "FileNotFoundError",
    "childprocer": "ChildProcessError",
    "uctraser": "UnicodeTranslateError",
    "isader": "IsADirectoryError",
    "unbdlaler": "UnboundLocalError",
    "ftper": "FloatingPointError",
    "connreser": "ConnectionResetError",
    "connateder": "ConnectionAbortedError",
    "connrefuseder": "ConnectionRefusedError",
    "pyfinaltioner": "PythonFinalizationError",
    "baseexgroup": "BaseExceptionGroup",
}

def transform_source(data: bytes) -> bytes:
    tokens = list(tokenize.tokenize(BytesIO(data).readline))
    new_tokens = []
    for ttype, tstring, start, end, line in tokens:
        if ttype == tokenize.NAME and tstring in RULES:
            new_tokens.append((ttype, RULES[tstring]))
        else:
            new_tokens.append((ttype, tstring))
    return tokenize.untokenize(new_tokens).encode("utf-8")

class MiniPyLoader(importlib.abc.SourceLoader):
    def __init__(self, path): self.path = path
    def get_filename(self, fullname): return self.path
    def get_data(self, path): return open(path, "rb").read()
    def source_to_code(self, data, path, *, _optimize=-1):
        return compile(transform_source(data), path, "exec", optimize=_optimize)

class MiniPyFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        import os
        filename = fullname.split(".")[-1] + ".py"
        for base in path or sys.path:
            candidate = os.path.join(base, filename)
            if os.path.isfile(candidate):
                loader = MiniPyLoader(candidate)
                return importlib.util.spec_from_loader(fullname, loader)
        return None

# 훅 설치
if not any(isinstance(x, MiniPyFinder) for x in sys.meta_path):
    sys.meta_path.insert(0, MiniPyFinder())
