# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sight_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'sight-api',
    'version': '1.2.0',
    'description': "Official client for Siftrics' Sight API, which is a text recognition service",
    'long_description': 'This repository contains the official [Sight API](https://siftrics.com/) Python client. The Sight API is a text recognition service.\n\n# Quickstart\n\n1. Install the package.\n\n```\npip install sight-api\n```\n\nor\n\n```\npoetry add sight-api\n```\n\netc.\n\n2. Grab an API key from the [Sight dashboard](https://siftrics.com/).\n3. Create a client, passing your API key into the constructor, and recognize text:\n\n```\nimport sight_api\n\nclient = sight_api.Client(\'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\')\n\npages = client.recognize([\'invoice.pdf\', \'receipt_1.png\'])\n```\n\n`pages` looks like this:\n\n```\n[\n    {\n        "Error": "",\n        "FileIndex": 0,\n        "PageNumber": 1,\n        "NumberOfPagesInFile": 3,\n        "RecognizedText": [ ... ]\n    },\n    ...\n]\n```\n\n`FileIndex` is the index of this file in the original request\'s "files" array.\n\n`RecognizedText` looks like this:\n\n```\n"RecognizedText": [\n    {\n        "Text": "Invoice",\n        "Confidence": 0.22863210084975458\n        "TopLeftX": 395,\n        "TopLeftY": 35,\n        "TopRightX": 449,\n        "TopRightY": 35,\n        "BottomLeftX": 395,\n        "BottomLeftY": 47,\n        "BottomRightX": 449,\n        "BottomRightY": 47,\n    },\n    ...\n]\n```\n\n## Streaming in Results\n\nIf you process more than one page in a single `.recognize([ ... ])` call, results may come in over time, instead of all at once.\n\nTo access results (`pages` objects) as soon as they come in, there is a generator you can use:\n\n```\nfor pages in self.recognizeAsGenerator([\'invoice.pdf\', \'receipt_1.png\']):\n    print(pages)\n```\n\nIn fact, `.recognize([ ... ])` is defined in terms of that generator:\n\n```\nclass Client:\n    ...\n    def recognize(self, files):\n        ...\n        pages = list()\n        for ps in self.recognizeAsGenerator(files):\n            pages.extend(ps)\n        return pages\n```\n\n## Word-Level Bounding Boxes\n\n`client.recognize(files, words=False)` has a parameter, `words`, which defaults to `False`, but if it\'s set to `True` then word-level bounding boxes are returned instead of sentence-level bounding boxes.\n\n### Auto-Rotate\n\nThe Sight API can rotate and return input images so the majority of the recognized text is upright. Note that this feature is part of the "Advanced" Sight API and therefore each page processed with this behavior enabled is billed as 4 pages. To enable this behavior, call the recognize function with the default parameter `autoRotate` set to `True`:\n\n```\npages = client.recognize([\'invoice.pdf\'], autoRotate=True)\n```\n\nNow, the `Base64Image` field will be set in the elements of `pages`.\n\n### Why are the bounding boxes are rotated 90 degrees?\n\nSome images, particularly .jpeg images, use the [EXIF](https://en.wikipedia.org/wiki/Exif) data format. This data format contains a metadata field indicating the orientation of an image --- i.e., whether the image should be rotated 90 degrees, 180 degrees, flipped horizontally, etc., when viewing it in an image viewer.\n\nThis means that when you view such an image in Chrome, Firefox, Safari, or the stock Windows and Mac image viewer applications, it will appear upright, despite the fact that the underlying pixels of the image are encoded in a different orientation.\n\nIf you find your bounding boxes are rotated or flipped relative to your image, it is because the image decoder you are using to load images in your program obeys EXIF orientation, but the Sight API ignores it (or vice versa).\n\nAll the most popular imaging libraries in Go, such as "image" and "github.com/disintegration/imaging", ignore EXIF orientation. You should determine whether your image decoder obeys EXIF orientation and tell the Sight API to do the same thing. You can tell the Sight API to obey the EXIF orientation by calling the recognize function with the default parameter `exifRotate` set to `True`:\n\n```\npages = client.recognize([\'invoice.pdf\'], exifRotate=True)\n```\n\nBy default, the Sight API ignores EXIF orientation.\n\n## Official API Documentation\n\nHere is the [official documentation for the Sight API](https://siftrics.com/docs/sight.html).\n\n# Apache V2 License\n\nThis code is licensed under Apache V2.0. The full text of the license can be found in the "LICENSE" file.\n',
    'author': 'Siftrics Founder',
    'author_email': 'siftrics@siftrics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://siftrics.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
