setup_args = {
    'name': 'qinfluxdb',
    'version': '0.1',
    'packages': ['qinfluxdb'],
    'url': 'https://github.com/unaizalakain/qinfluxdb',
    'description': 'A little ORM for issuing queries to InfluxDB',
    'long_description': open('README.rst').read(),
    'author': 'Unai Zalakain',
    'author_email': 'unai@gisa-elkartea.org',
    'maintainer': 'Unai Zalakain',
    'maintainer_email': 'unai@gisa-elkartea.org',
    'license': 'GPLv3',
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Database :: Front-Ends',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
}


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
else:
    setup_args['install_requires'] = ['influxdb']

setup(**setup_args)
