import os
import re
import sys
from Cython.Build import cythonize
from Cython.Compiler import Options
from distutils.core import Extension, setup

__ABS_DIR_PATH = os.path.abspath('')
exclude_so = ["__init__.py", "setup.py", "main.py", "gunicorn.py"]
sources = ['./']

extensions = []
sources_files = []
for source in sources:
    for dir_path, folder_names, filenames in os.walk(source):
        for filename in filter(lambda x: re.match(r'.*[.]py$', x), filenames):
            print(filename)
            file_path = os.path.join(dir_path, filename)
            print(file_path)
            if filename not in exclude_so:
                sources_files.append(file_path)
            if filename not in exclude_so:
                print("debug point ", file_path[:-3].replace('/', '.')[2:])
                extensions.append(
                    Extension(file_path[:-3].replace('/', '.')[2:], [file_path], extra_compile_args=["-Os", "-g0"],
                              extra_link_args=["-Wl,--strip-all"]))

print(sources_files)
Options.docstrings = False
compiler_directives = {'optimize.unpack_method_calls': False, 'always_allow_keywords': True}

try:
    setup(
        ext_modules=cythonize(
            extensions,
            exclude=None,
            nthreads=20,
            quiet=True,
            language_level=3,
            compiler_directives=compiler_directives
        )
    )
    print("Start remove source files...")
    for sf in sources_files:
        os.remove(sf)
        os.remove('{}.c'.format(sf[:-3]))
except Exception as ex:
    print("error! ", str(ex))
    sys.exit(1)
