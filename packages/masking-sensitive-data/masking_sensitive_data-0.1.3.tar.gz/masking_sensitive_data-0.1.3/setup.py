import re

from setuptools import setup, find_packages

with open('masking_sensitive_data/__init__.py') as ver_file:
    ver = re.compile(r".*__version__ = '(.*?)'", re.S).match(ver_file.read())
    if ver is not None:
        version = ver.group(1)
    else:
        version = '0.0.0'

with open('requirements_ipapp.txt') as requirements_file:
      requirements_ipapp = requirements_file.read()

setup(
      name='masking_sensitive_data',
      version='0.1.3',
      description='Package for capturing and masking sensitive data',
      url='',
      classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: System Administrators',
            'Operating System :: Unix',
            'Operating System :: POSIX :: Linux',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Internet',
      ],
      author='InPlat',
      python_requires='>=3.7',
      packages=find_packages('.', exclude=['tests']),
      extras_require={'ipapp': requirements_ipapp.split('\n')},
      zip_safe=False
)
