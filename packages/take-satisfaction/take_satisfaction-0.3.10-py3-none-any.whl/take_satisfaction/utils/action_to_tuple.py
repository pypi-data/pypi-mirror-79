__author__ = 'Milo Utsch'
__version__ = '0.1.0'

import typing as tp


def action_to_tuple(actions: tp.Any) -> tp.Tuple[str]:
    """Converts list of strings into a tuple of actions.
    
    Raises an TypeError exception should it contain unexpected types.
    
    :param actions: List of strings to be converted into tuple.
    :type actions: ``list`` from ``any``
    :return: Tuple containing the passed strings.
    :rtype: ``tuple``
    """
    if all(isinstance(item, str) for item in actions):
        return tuple(actions)
    else:
        raise TypeError(f'Actions parameter should only contain strings')
