__author__ = 'Moises Mendes, Gabriel Salgado and Milo Utsch'
__version__ = '0.1.2'

import json
import typing as tp


def load_params() -> tp.Dict[str, tp.Any]:
    """Function to load parameters from conf/base.

    :return: Dict containing all parameters.
    :rtype: ``dict`` from ``str`` to ``any``
    """
    return json.load(open('conf/base/params.json'))
