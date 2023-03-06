import setuptools

import jocasta

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='jocasta',
    version=jocasta.__version__,
    author='Chris Hannam',
    author_email='ch@chrishannam.co.uk',
    description='Fetch sensor data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chrishannam/jocasta',
    packages=setuptools.find_packages(exclude=('tests', 'examples')),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'click',
        'influxdb-client',
        'pyserial5',
        'psutil',
        'tabulate',
        # 'pycryptodome',
        'tapo-plug',
        'confluent-kafka'
    ],
    include_package_data=True,
    entry_points={'console_scripts': ['jocasta=jocasta.collector:main', 'tapo=jocasta.tapo:main']},
)
