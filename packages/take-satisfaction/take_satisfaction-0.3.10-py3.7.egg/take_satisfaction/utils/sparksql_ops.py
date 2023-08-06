__author__ = 'Gabriel Salgado and Milo Utsch'
__version__ = '0.1.3'
__all__ = [
    'DF',
    'SDF',
    'CONTEXT',
    'query_df',
    'spark_to_pandas',
    'retrieve_data'
]

import typing as tp
import warnings as wn

import pandas as pd
with wn.catch_warnings():
    wn.simplefilter('ignore')
    import pyspark as ps

from take_satisfaction.utils import action_to_tuple

DF = pd.DataFrame
SDF = ps.sql.DataFrame
CONTEXT = ps.sql.HiveContext


def retrieve_data(sql_context: CONTEXT, simple_query: str, actions_query: str, actions: tp.List[any], **kwargs) -> DF:
    """Verifies the actions parameters and do the suitable query.

    :param sql_context: Context for spark.
    :type sql_context: ``pyspark.sql.HiveContext``
    :param simple_query: Query that does not require an action list.
    :type simple_query: ``str``
    :param actions_query: Query that requires an action list.
    :type actions_query: ``str``
    :param actions: List of actions to be used on the query.
    :type actions: ``list`` from ``str``
    :param kwargs: To be used on query.format.
    :type kwargs: ``str``
    :return: Pyspark dataframe with query.
    :rtype: ``pyspark.sql.DataFrame``
    """
    if actions:
        actions = action_to_tuple(actions)
        return query_df(sql_context=sql_context, query=actions_query, actions=actions, **kwargs)
    else:
        return query_df(sql_context=sql_context, query=simple_query, **kwargs)
    

def query_df(sql_context: CONTEXT, query: str, **kwargs: tp.Any) -> SDF:
    """Do a query on HIVE spark.
    
    :param sql_context: Context for spark.
    :type sql_context: ``pyspark.sql.HiveContext``
    :param query: Query as formatter string.
    :type query: ``str``
    :param kwargs: To be used on query.format.
    :type kwargs: ``any``
    :return: Pyspark dataframe with query.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return sql_context.sql(query.format(**kwargs))


def spark_to_pandas(df: SDF) -> DF:
    """Query spark dataframe getting pandas dataframe.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :return: Pandas dataframe with the data.
    :rtype: ``pandas.DataFrame``
    """
    return df.toPandas()
