# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyloopenergy']

package_data = \
{'': ['*']}

install_requires = \
['socketIO-client-nexus==0.7.6']

setup_kwargs = {
    'name': 'pyloopenergy',
    'version': '0.1.5',
    'description': 'Access Loop Energy energy monitors via Socket.IO API',
    'long_description': 'PyLoopEnergy\n======\n\nThis provides a python API to [Loop Energy](https://www.your-loop.com) who provide electricity and gas monitors.\n\nIt uses their service to provide readings that are updated every 10 seconds for electricity, and every 15 minutes for gas.\n\nTo use the service you need the the client serial number and secret keys for your devices.\n\nYou can get this by logging into your-loop.com, opening your browser\'s console, and typing in ```Drupal.settings.navetas_realtime```.\n\n(There is more detailed documentation about how to do this here https://home-assistant.io/components/sensor.loop_energy/)\n\n*You should keep your secret keys,* **secret!**\n\nThanks to Marcos Scriven for producing a node implementation that I\'ve shamelessly copied. https://github.com/marcosscriven/loop\n\nData is returned in kw.\n\nDependencies\n------------\nPyLoopEnergy depends on socketIO-client. It needs version 0.5.6 which supports socket.IO version 0.9, rather than 1.0.\n\n\nHow to use\n----------\n\n    >> import pyloopenergy\n    >> elec_serial = \'your serial\'\n    >> elec_secret = \'your_secret\'\n    >> le = pyloopenergy.LoopEnergy(elec_serial, elec_secret)\n    >> le.electricity_useage\n\n    0.602\n\n    >> le.terminate()\n\nNotes:\n 1. Data is fetched asynchronously, so `le` may not be populated if you call `electricity_useage` straight after creating it. The API provides callback functions on update (there is a simple example below).\n 2. It can take 15s to terminate the monitoring thread after calling `terminate`.\n\n\nSimple subscription example\n---------\n````\nimport pyloopenergy\nimport time\n\ndef gas_trace():\n    print("Gas =", le.gas_useage)\n\ndef elec_trace():\n    print("Electricity =", le.electricity_useage)\n\nelec_serial = \'00000\';\nelec_secret = \'YYYYYY\';\n\ngas_serial = \'11111\';\ngas_secret = \'ZZZZZ\';\n\nle = pyloopenergy.LoopEnergy(elec_serial, elec_secret, gas_serial, gas_secret)\nle.subscribe_gas(gas_trace)\nle.subscribe_elecricity(elec_trace)\n\ntime.sleep(120)\nle.terminate()\ntime.sleep(60)\n````\nThis produces the following output.\n\n````\nElectricity = 1.13\nGas = 0.0\nElectricity = 1.116\n````\n\nGas Meter Types and Calorific values\n---------\n\nThe library supports metric and imperial gas meters (reading cubic metres or 100s of cubic feet)\n\nThe default is a metric meter, but you can specify an imperial or metric meter.\n\n````\nle = pyloopenergy.LoopEnergy(elec_serial, elec_secret, gas_serial, gas_secret, pyloopenergy.IMPERIAL)\n\nle = pyloopenergy.LoopEnergy(elec_serial, elec_secret, gas_serial, gas_secret, pyloopenergy.METRIC)\n\n````\n\nTo convert from a volume reading into kw, the library needs to know how much energy is in each metre of gas. The default is 39.11, but you can use the real number from your supplier if you like.\n\n````\nle = pyloopenergy.LoopEnergy(elec_serial, elec_secret, gas_serial, gas_secret, pyloopenergy.IMPERIAL, 39.1)\n\nle = pyloopenergy.LoopEnergy(elec_serial, elec_secret, gas_serial, gas_secret, pyloopenergy.METRIC, 39.1)\n\n````\n\n\n',
    'author': 'Greg Dowling',
    'author_email': 'mail@gregdowling.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/pavoni/pyloopenergy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
