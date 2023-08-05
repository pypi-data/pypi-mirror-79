# To install locally: python setup.py build && python setup.py install
# (If there are problems with installation of the documentation, it may be that
#  the egg file is out of sync and will need to be manually deleted -
#  see error message for details of the corrupted zip file. )
#
# To push a version through to pip.
#  - Make sure it installs correctly locally as above
#  - Update the version information in this file
#  - python setup.py sdist ; twine upload dist/*  
# Note: replace * with the actual tar file if network limited !
#
# (see http://peterdowns.com/posts/first-time-with-pypi.html)


from setuptools import setup

try: 
    from distutils.command import bdist_conda
except ImportError:
    pass


from os import path
import io

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if __name__ == "__main__":
    setup(name='litho1pt0',
          author            = "LM",
          author_email      = "louis.moresi@unimelb.edu.au",
          url               = "https://github.com/underworldcode/litho1pt0",
          download_url      = "",
          version           = "1.5.0",
          description       = "Python interface to Litho 1.0 dataset - based on stripy",
          long_description  =long_description,
          long_description_content_type='text/markdown',
          packages          = ['litho1pt0'],
          package_dir       = {'litho1pt0': 'litho1pt0'},
          package_data      = {'litho1pt0': ['data/*.npz', 'Notebooks/litho1pt0/*ipynb', 'Notebooks/litho1pt0/data/*nc'] },
          include_package_data = True,
          install_requires=['stripy']
          )
