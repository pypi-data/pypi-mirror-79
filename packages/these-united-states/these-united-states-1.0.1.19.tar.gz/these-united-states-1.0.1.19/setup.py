# BSD 3-Clause License
#
# Copyright (c) 2020, 8minute Solar Energy LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Setup script for these-united-states"""

from distutils.command.build import build as _build
from distutils.dep_util import newer_group
from distutils import log
import pathlib
import shutil

from setuptools import Command, find_packages, setup


DATA_YEAR = 2019


class download(Command):
    description = 'download the shape file'
    user_options = [
        ('build-temp=', 't',
         'directory for temporary files (build by-products)'),
        ('force', 'f',
         'download the shape file even if it already exists'),
    ]

    def initialize_options(self):
        self.build_temp = None
        self.force = None

    def finalize_options(self):
        self.set_undefined_options(
            'build',
            ('build_temp', 'build_temp'),
            ('force', 'force'),
        )

    def run(self):
        import requests

        url = f'https://www2.census.gov/geo/tiger/TIGER{DATA_YEAR}/STATE/tl_{DATA_YEAR}_us_state.zip'
        path = pathlib.Path(self.build_temp, url.rsplit('/', 1)[-1])
        if not self.force and path.exists():
            log.debug(f'skipping download; {path} exists')
            return
        if not path.parent.exists():
            self.mkpath(str(path.parent))
        log.info(f'downloading {url}')
        if not self.dry_run:
            with requests.get(url, stream=True) as response, path.open('wb') as file:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file)


class build_data(Command):
    description = 'convert shape file to points data file'
    user_options = [
        ('build-lib=', 'b',
         "directory for compiled extension modules"),
        ('build-temp=', 't',
         'directory for temporary files (build by-products)'),
        ('force', 'f',
         "forcibly build everything (ignore file timestamps)"),
        ('inplace', 'i',
         'ignore build-lib and put compiled extensions into the source '
         'directory alongside your pure Python modules'),
    ]

    def initialize_options(self):
        self.build_lib = None
        self.build_temp = None
        self.force = None
        self.inplace = None

    def finalize_options(self):
        self.set_undefined_options(
            'build',
            ('build_lib', 'build_lib'),
            ('build_temp', 'build_temp'),
            ('force', 'force'),
        )
        if self.inplace is None:
            self.inplace = True

    def run(self):
        name, = self.distribution.packages
        dest_path = (pathlib.Path(__file__).parent if self.inplace else pathlib.Path(self.build_lib))
        zip_path = pathlib.Path(self.build_temp, f'tl_{DATA_YEAR}_us_state.zip')
        shapes_path = dest_path / f'{name}/shapes.zip'
        if self.force or newer_group([shapes_path], zip_path, 'newer'):
            if not zip_path.exists():
                self.run_command('download')
            self.copy_file(zip_path, shapes_path)


class build(_build):
    sub_commands = [
        ('download', lambda _: True),
        ('build_data', lambda _: True),
    ] + _build.sub_commands


with open('README.md') as file:
    long_description = file.read()


setup(
    name='these-united-states',
    version=f'1.0.1.{DATA_YEAR % 100}',
    python_requires='>=3.6',

    packages=find_packages(include=['united_states']),

    include_package_data=True,
    package_data={
        'united_states': ['shapes.zip', 'py.typed'],
    },

    install_requires=[
        # pyshp v2.1.1 enabled logging of all warnings for all packages
        # See https://github.com/GeospatialPython/pyshp/issues/203
        'pyshp >= 2, < 3, != 2.1.1',
        'importlib_resources;python_version<"3.7"',
    ],

    extras_require={
        'cli': ['click >= 7.1, < 8'],
        'plot': ['matplotlib >= 3.2, < 4']
    },

    setup_requires=[
        'requests >= 2.22, < 3',
        'setuptools',
        'wheel',
    ],

    author='Brandon Carpenter',
    author_email='brandon@8minute.com',
    url='https://bitbucket.org/8minutenergy/these-united-states',
    description='Utility library for performing reverse geocoding of states in the United States of America',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='BSD',
    zip_safe=True,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: GIS',
        'Typing :: Typed',
    ],

    cmdclass={
        'build': build,
        'build_data': build_data,
        'download': download,
    }
)
