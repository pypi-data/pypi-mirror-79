# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywemo',
 'pywemo.ouimeaux_device',
 'pywemo.ouimeaux_device.api',
 'pywemo.ouimeaux_device.api.xsd']

package_data = \
{'': ['*']}

install_requires = \
['ifaddr>=0.1.0', 'requests>=2.0', 'six>=1.10.0']

setup_kwargs = {
    'name': 'pywemo',
    'version': '0.5.0',
    'description': 'Lightweight Python module to discover and control WeMo devices',
    'long_description': 'pyWeMo |Build Badge| |PyPI Version Badge| |PyPI Downloads Badge|\n================================================================\nLightweight Python 2 and Python 3 module to discover and control WeMo devices.\n\nThis is a stripped down version of the Python API for WeMo devices, `ouimeaux <https://github.com/iancmcc/ouimeaux>`_, with simpler dependencies.\n\nDependencies\n------------\npyWeMo depends on Python packages: requests, ifaddr and six\n\nHow to use\n----------\n\n.. code:: python\n\n    >> import pywemo\n\n    >> devices = pywemo.discover_devices()\n    >> print(devices)\n    [<WeMo Insight "AC Insight">]\n\n    >> devices[0].toggle()\n    \n    \nIf discovery doesn\'t work on your network\n-----------------------------------------\nOn some networks discovery doesn\'t work reliably, in that case if you can find the ip address of your Wemo device you can use the following code.\n\n.. code:: python\n\n    >> import pywemo\n    \n    >> address = "192.168.100.193"\n    >> port = pywemo.ouimeaux_device.probe_wemo(address)\n    >> url = \'http://%s:%i/setup.xml\' % (address, port)\n    >> device = pywemo.discovery.device_from_description(url, None)\n    >> print(device)\n    <WeMo Insight "AC Insight">\n    \nPlease note that you need to use ip addresses as shown above, rather than hostnames, otherwise the subscription update logic won\'t work.\n\nLicense\n-------\nThe code in pywemo/ouimeaux_device is written and copyright by Ian McCracken and released under the BSD license. The rest is released under the MIT license.\n\n.. |Build Badge| image:: https://travis-ci.org/pavoni/pywemo.svg?branch=master\n   :target: https://travis-ci.org/pavoni/pywemo\n   :alt: Status of latest Travis CI build\n.. |PyPI Version Badge| image:: https://pypip.in/v/pywemo/badge.png\n    :target: https://pypi.org/project/pywemo/\n    :alt: Latest PyPI version\n.. |PyPI Downloads Badge| image:: https://pypip.in/d/pywemo/badge.png\n    :target: https://pypi.org/project/pywemo/\n    :alt: Number of PyPI downloads\n',
    'author': 'Greg Dowling',
    'author_email': 'mail@gregdowling.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pavoni/pywemo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
