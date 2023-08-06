__author__ = 'Gabriel Salgado, Juliana Guamá, Milo Utsch e Rogers Damas'
__version__ = '0.3.10'

import typing as tp

from take_satisfaction.utils import CONTEXT
from take_satisfaction.utils import load_params
from take_satisfaction.utils import retrieve_data
from take_satisfaction.utils import spark_to_pandas
from take_satisfaction.preprocess import complete_scale
from take_satisfaction.preprocess import remove_manual
from take_satisfaction.conversion import convert_scale
from take_satisfaction.calculation import calculate_satisfaction_rate


def run(sql_context: CONTEXT, bot_identity: str,
        start_date: str = '', end_date: str = '', category: str = '',
        **kwargs) -> tp.Dict[str, tp.Any]:
    """Run Take Satisfaction
    
    :param sql_context: Context for spark.
    :type sql_context: ``pyspark.sql.HiveContext``
    :param bot_identity: Bot identity on database.
    :type bot_identity: ``str``
    :param start_date: Beginning date to filter ("yyyy-mm-dd"). Default value is str()
    :type start_date: ``str``
    :param end_date: Ending date to filter ("yyyy-mm-dd"). Default value is str()
    :type end_date: ``str``
    :param category: Satisfaction Survey tracking name on database. Default value is str()
    :type category: ``str``
    :param kwargs: Parameters to overwrite configuration parameters.
    :type kwargs: ``any``
    :return: Parameters and results for MLFlow register.
    :rtype: ``dict`` from ``str`` to ``any``
    """
    params = load_params()
    params.update(kwargs)

    actions = params['actions']
    databricks_query = params['databricks_query']
    databricks_actions_query = params['databricks_actions_query']
    bot_events_answer_column = params['bot_events_answer_column']
    bot_events_quantities_column = params['bot_events_quantities_column']
    
    sp_df = retrieve_data(sql_context=sql_context,
                          simple_query=databricks_query,
                          actions_query=databricks_actions_query,
                          actions=actions,
                          answer=bot_events_answer_column,
                          quantities=bot_events_quantities_column,
                          start_date=start_date,
                          end_date=end_date,
                          bot_identity=bot_identity,
                          category=category)
    scale_raw_df = spark_to_pandas(df=sp_df)

    missing_quantity = params['missing_quantity']
    scale_raw_completed_df = complete_scale(sp_df,
                                            bot_events_answer_column,
                                            bot_events_quantities_column,
                                            actions,
                                            missing_quantity)
    
    scale_manual = params['scale_manual']
    similarity_threshold = params['similarity_threshold']
    preprocessed_df = remove_manual(df=scale_raw_completed_df,
                                    manual_entries=scale_manual,
                                    threshold=similarity_threshold,
                                    column=bot_events_answer_column)
    
    scale_translations = params['scale_translations']
    converted_df = convert_scale(df=preprocessed_df,
                                 column=bot_events_answer_column,
                                 reference=scale_translations,
                                 threshold=similarity_threshold)

    satisfaction_rate = calculate_satisfaction_rate(df=converted_df,
                                                    level_column=bot_events_answer_column,
                                                    quantities_column=bot_events_quantities_column)
    
    return {
        'params': params,
        'result': {
            'raw': {
                'scale': scale_raw_df
            },
            'primary': {
                'preprocessed': preprocessed_df
            },
            'features': {
                'converted': converted_df
            },
            'model_input': {
                'satisfaction_rate': satisfaction_rate
            },
        }
    }
