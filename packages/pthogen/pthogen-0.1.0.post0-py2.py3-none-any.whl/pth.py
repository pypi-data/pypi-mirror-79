import sys
import importlib

if sys.version_info >= (3, 7):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata

def run():
    for ep in sorted(eps.get("pth"), key=lambda x: (x.name, x.value)):
        ep.load()()
