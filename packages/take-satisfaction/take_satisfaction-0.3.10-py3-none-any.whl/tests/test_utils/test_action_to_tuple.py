__author__ = 'Milo Utsch'
__version__ = '0.1.0'

import pytest

from take_satisfaction.utils import *


def test_action_to_tuple_success():
    mock_action_list = ['Ajudou', 'Não Ajudou']
    
    result = action_to_tuple(mock_action_list)
    
    expected_result = ('Ajudou', 'Não Ajudou')
    
    assert expected_result == result


def test_action_to_tuple_failure():
    mock_action_list = [200, 'Não Ajudou']

    with pytest.raises(TypeError, match=r'.*Actions parameter should only contain strings'):
        action_to_tuple(mock_action_list)
