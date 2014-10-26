# setup.py
from distutils.core import setup
import py2exe

setup(console=["echess.py"],
      data_files=[('komodo-5-64bit.exe'),
                  ('stockfish_14053109_x64.exe'),
                  ('Gull 3 x64.exe'), ('Houdini_15a_x64.exe')])

