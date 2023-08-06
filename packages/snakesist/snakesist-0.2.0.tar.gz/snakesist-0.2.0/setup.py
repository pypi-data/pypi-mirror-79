# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakesist']

package_data = \
{'': ['*']}

install_requires = \
['delb[https-loader]>=0.2,<0.3']

entry_points = \
{'delb': ['snakesist = snakesist.delb_plugins']}

setup_kwargs = {
    'name': 'snakesist',
    'version': '0.2.0',
    'description': 'A Python database interface for eXist-db',
    'long_description': '.. image:: https://i.ibb.co/JsZqM7z/snakesist-logo.png\n    :target: https://snakesist.readthedocs.io\n\nsnakesist\n=========\n\n.. image:: https://badge.fury.io/py/snakesist.svg\n    :target: https://badge.fury.io/py/snakesist\n\n.. image:: https://readthedocs.org/projects/snakesist/badge/?version=latest\n    :target: https://snakesist.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://travis-ci.org/03b8/snakesist.svg?branch=master\n    :target: https://travis-ci.org/03b8/snakesist\n\n\n``snakesist`` is a Python database interface for `eXist-db <https://exist-db.org>`_.\nIt supports basic CRUD operations and uses `delb <https://delb.readthedocs.io>`_ for representing the yielded resources.\n\n.. code-block:: shell\n\n    pip install snakesist\n\n``snakesist`` allows you to access individual documents from the database using a ``delb.Document`` object, either by simply passing a URL\n\n.. code-block:: python\n\n    >>> from delb import Document\n\n    >>> manifest = Document("existdb://admin:@localhost:8080/exist/db/manifestos/dada_manifest.xml")\n    >>> [header.full_text for header in manifest.xpath("//head")]\n    ["Hugo Ball", "Das erste dadaistische Manifest"]\n\nor by passing a relative path to the document along with a database client which you can subsequently reuse\n\n.. code-block:: python\n\n    >>> from snakesist import ExistClient\n\n    >>> my_local_db = ExistClient(host="localhost", port=8080, user="admin", password="", root_collection="/db/manifests")\n    >>> dada_manifest = Document("dada_manifest.xml", existdb_client=my_local_db)\n    >>> [header.full_text for header in dada_manifest.xpath("//head")]\n    ["Hugo Ball", "Das erste dadaistische Manifest"]\n    >>> communist_manifest = Document("communist_manifest.xml", existdb_client=my_local_db)\n    >>> communist_manifest.xpath("//head").first.full_text\n    "Manifest der Kommunistischen Partei"\n\n\nand not only for accessing individual documents, but also for querying data across multiple documents\n\n.. code-block:: python\n\n    >>> all_headers = my_local_db.xpath("//*:head")\n    >>> [header.node.full_text for header in all_headers]\n    ["Hugo Ball", "Das erste dadaistische Manifest", "Manifest der Kommunistischen Partei", "I. Bourgeois und Proletarier.", "II. Proletarier und Kommunisten", "III. Sozialistische und kommunistische Literatur", "IV. Stellung der Kommunisten zu den verschiedenen oppositionellen Parteien"]\n\nYou can of course also modify and store documents back into the database or create new ones and store them.\n\n\nYour eXist instance\n-------------------\n\n``snakesist`` leverages the\n`eXist RESTful API <https://www.exist-db.org/exist/apps/doc/devguide_rest.xml>`_\nfor database queries. This means that allowing database queries using the\n``_query`` parameter of the RESTful API is a requirement in the used eXist-db\nbackend. eXist allows this by default, so if you haven\'t configured your\ninstance otherwise, don\'t worry about it.\n\nPlease note that ``snakesist`` is tested with eXist 4.7.1 and is not compatible yet\nwith version 5. The bug preventing ``snakesist`` to be compatible with the newest major eXist\nversion will be fixed with the release of eXist 5.3.0.\n',
    'author': 'Theodor Costea',
    'author_email': 'theo.costea@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/03b8/snakesist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
