# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tcpchan', 'tcpchan.aio', 'tcpchan.core']

package_data = \
{'': ['*']}

install_requires = \
['fpack>=1.0.0']

setup_kwargs = {
    'name': 'tcpchan',
    'version': '0.1.1',
    'description': 'tcpchan is a TCP (de)multiplexer',
    'long_description': 'TCPChan\n====\n\n[![PyPI version](https://badge.fury.io/py/tcpchan.svg)](https://badge.fury.io/py/tcpchan)\n\n***TCPChan*** is a TCP connection multiplexing library that enables working with multiple *channels* in a single TCP connection. TCPChan can boost the efficiency of the short-lived connections by eliminating the overhead of connection setup, especially in high-latency links (e.g. cross-continental links).\n\nThe core part of the library is decoupled from I/O libraries so it\'s possible to bring your own I/O library. For convenience, an Asyncio-based protocol implementation is provided for easy integration with Asyncio applications.\n\nWarning: TCPChan is built for fun and educational purpose, it is not fully tested, and neither is it widely deployed. Use it at your own risk.\n\n## Guide\nWIP\n\n### Installation\n#### Install via Pip\n```bash\npip install tcpchan\n```\n\n#### Install latest version from GitHub\n```basb\ngit clone --depth 1 https://github.com/frankurcrazy/tcpchan\ncd tcpchan; python setup.py install\n```\n\n#### Dependencies\n1. python >= 3.7\n1. fpack >= 1.0.0\n\n### Usage\nWIP\n\n#### Channel\nInherit `tcpchan.core.chan.Channel` and implements `data_received` callback.\n```python\nfrom tcpchan.core.chan import Channel\n\nclass CustomChannel(Channel):\n    def data_received(self, data):\n        # Do stuff upon data reception\n```\n\n#### Connection\nCreate `ServerConnection` or `ClientConnection` instance upon connection establishment in server/client. And pass the channel factory to the Connection.\n\n##### Server connection creation\n```python\nfrom tcpchan.core.conn import ServerConnection\n\nconn = ServerConnection(lambda: CustomChannel())\n```\n\n##### Client connection creation\n```python\nfrom tcpchan.core.conn import ClientConnection\n\nconn = ClientConnection(lambda: CustomChannel())\n```\n\n#### Events\n```python\nfrom tcpchan.core import (\n    HandshakeSuccess, DataTransmit,\n    ChannelCreated, ChannelClosed\n)\n```\n\n#### Asyncio\nTCPChan provides an Asyncio-based protocol implementation so that one can easily integrate TCPChan in their Asyncio applications.\n\nFor server-side application, `TCPChanServerProtocol` can be used, likewise, for client-side application, `TCPChanClientProtocol` can be used.\n\n```python\nimport asyncio\nfrom tcpchan.aio import TCPChanServerProtocol\nfrom tcpchan.core.chan import Channel\n\n\nclass CustomChannel(Channel):\n    def data_received(self, data):\n        # Do stuff upon data reception\n        ...\n\n\nclass MyProtocol(TCPChanServerProtocol):\n    def __init__(self, *args, **kwargs):\n        super().__init__(*args, **kwargs)\n\n        self._channels = {}  # Mapping for channels\n\n    def handshake_success(self):\n        # Do something on handshake success\n        ...\n\n    def handshake_failed(self, reason):\n        # Do something on handshake failure\n        ...\n\n    def channel_created(self, channel):\n        # Do something on channel creation\n        self._channels[channel.channel_id] = channel\n\n    def channel_closed(self, channel_id):\n        # Do something when a channel is closed\n        del self._channels[channel_id]\n\n\nloop = asyncio.get_event_loop()\n\n\n# To initialize `Protocol`, channel factory function is required.\nserver = await loop.create_server(\n    lambda: MyProtocol(lambda: CustomChannel()),\n    host="localhost",\n    port=9487,\n    start_serving=True,\n)\nloop.run_forever()\n```\n\n## LICENSE\nBSD\n',
    'author': 'Frank Chang',
    'author_email': 'frank@csie.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frankurcrazy/tcpchan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
