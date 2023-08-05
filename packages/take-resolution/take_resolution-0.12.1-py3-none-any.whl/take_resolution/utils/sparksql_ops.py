__author__ = 'Moises Mendes and Gabriel Salgado'
__version__ = '0.7.0'
__all__ = [
    'CONTEXT',
    'DF',
    'SDF',
    'SS',
    'build_dataframe',
    'build_from_jdbc',
    'count',
    'difference_between_rows',
    'distinct',
    'div',
    'filter_conditioned_rows',
    'filter_range_rows',
    'filter_rows',
    'filter_rows_not_equal',
    'group_by',
    'join',
    'query_spark_sql',
    'select_columns',
    'spark_to_pandas',
]

import typing as tp
import operator as op
import functools as ft
import warnings as wn

import pandas as pd
with wn.catch_warnings():
    wn.simplefilter('ignore')
    import pyspark as ps
    from pyspark.sql.window import Window
    import pyspark.sql.functions as f

CONTEXT = ps.SQLContext
DF = pd.DataFrame
GROUPED = ps.sql.GroupedData
SDF = ps.sql.DataFrame
SS = ps.sql.session.SparkSession


def build_dataframe(sql_context: CONTEXT, database: str, table: str) -> SDF:
    """Build Pyspark DataFrame from Spark SQL context.

    :param sql_context: Pyspark SQL context to connect to database and table.
    :type sql_context: ``pyspark.SQLContext``
    :param database: Database name.
    :type database: ``str``
    :param table: Table name.
    :type table: ``str``
    :return: Pyspark DataFrame pointing to specified table.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return sql_context.table(f'{database}.{table}')


def build_from_jdbc(spark_session: SS, jdbc_url: str, table: str, user: str, password: str,
                    integrated_security: str) -> SDF:
    """Build PySpark DataFrame from spark connection with SQL Server driver.

    :param spark_session: Spark Session to connect to table.
    :type spark_session: ``pyspark.sql.session.SparkSession``
    :param jdbc_url: URL to connect to database.
    :type jdbc_url: ``str``
    :param table: Table name.
    :type table: ``str``
    :param user: User to access table.
    :type user: ``str``
    :param password: Password to access table.
    :type password: ``str``
    :param integrated_security: Flag to set integrated security.
    :type integrated_security: ``str``
    :return: Pyspark DataFrame pointing to specified table.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return (
        spark_session.read.format('jdbc')
            .option('url', jdbc_url)
            .option('dbtable', table)
            .option('user', user)
            .option('password', password)
            .option('integratedSecurity', integrated_security)
            .load()
    )


def count(grouped: GROUPED) -> SDF:
    """Count elements by group on grouped data.
    
    :param grouped: Spark grouped data.
    :type grouped: ``pyspark.sql.GroupedData``
    :return: Spark dataframe with quantities by group.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return grouped.count()


def difference_between_rows(df: SDF, order_column: str, difference_column: str, result_column: str) -> SDF:
    """Calculate the difference between consecutive rows in `difference_column` of dataframe.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.DataFrame``
    :param order_column: Column informing order of records.
    :type order_column: ``str``
    :param difference_column: Column for which the difference is calculated.
    :type difference_column: ``str``
    :param result_column: Column name in which the result is saved.
    :type result_column: ``str``
    :return: Spark dataframe with consecutive difference column.
    :rtype: ``pyspark.DataFrame``
    """
    order_window = Window.orderBy(order_column)
    prev_column = f'{difference_column}_prev'
    
    df = df.withColumn(prev_column, f.lag(df[difference_column]).over(order_window))
    df = df.withColumn(result_column, (df[difference_column] - df[prev_column]))
    
    df = df.withColumn(result_column, f.coalesce(df[result_column], df[difference_column]))
    return df.drop(prev_column)


def distinct(df: SDF) -> SDF:
    """Remove duplicates on pyspark dataframe.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :return: Spark dataframe with no duplicates.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.distinct()


def div(df: SDF, column_1: str, column_2: str, result_column: str) -> SDF:
    """Divide `column_1` by `column_2` for each row and save it on `result_column`.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param column_1: Column with numerator.
    :type column_1: ``str``
    :param column_2: Column with denominator.
    :type column_2: ``str``
    :param result_column: Column for result.
    :type result_column: ``str``
    :return: Spark dataframe with division result.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.withColumn(result_column, df[column_1] / df[column_2])


def filter_conditioned_rows(df: SDF, columns_values: tp.List[tp.List[tp.Tuple[str, tp.Any]]]) -> SDF:
    """Filter rows of pyspark dataframe by satisfy any of group of pairs (column, value).
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param columns_values: Groups of pairs of column and value to be filtered.
    :type columns_values: ``list`` of ``list`` of (``str``, ``any``)
    :return: Filtered spark dataframe.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.filter(ft.reduce(op.or_, [
        ft.reduce(op.and_, [df[column] == value for column, value in column_value])
        for column_value in columns_values
    ]))


def filter_range_rows(df: SDF, column: str, lower: tp.Any, upper: tp.Any) -> SDF:
    """Filter rows of pyspark dataframe within the range of lower and upper value (inclusive).

    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param column: Column to be filtered.
    :type column: ``str``
    :param lower: Lower value to be filtered.
    :type lower: ``any``
    :param upper: Upper value to be filtered.
    :type upper: ``any``
    :return: Filtered spark dataframe.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.filter((df[column] >= lower) & (df[column] <= upper))


def filter_rows(df: SDF, *column_value: tp.Tuple[str, tp.Any]) -> SDF:
    """Filter rows of pyspark dataframe by each pair of (column, value).
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param column_value: Pairs of column and value to be filtered.
    :type column_value: (``str``, ``any``)
    :return: Filtered spark dataframe.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.filter(ft.reduce(op.and_, [df[column] == value for column, value in column_value]))


def filter_rows_not_equal(df: SDF, *column_value: tp.Tuple[str, tp.Any]) -> SDF:
    """Filter rows of pyspark dataframe to each column be not equal to each value.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param column_value: Pairs of column and value to be filtered.
    :type column_value: (``str``, ``any``)
    :return: Filtered spark dataframe.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.filter(ft.reduce(op.and_, [df[column] != value for column, value in column_value]))


def group_by(df: SDF, *columns: str) -> GROUPED:
    """Group a pyspark dataframe by given columns.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param columns: Columns to group by.
    :type columns: ``str``
    :return: Spark grouped data.
    :rtype: ``pyspark.sql.GroupedData``
    """
    return df.groupby(*columns)


def join(df_1: SDF, df_2: SDF, column_1: str, column_2: str, type: str) -> SDF:
    """Join two dataframes.
    
    :param df_1: Left spark dataframe.
    :type df_1: ``pyspark.sql.DataFrame``
    :param df_2: Right spark dataframe.
    :type df_2: ``pyspark.sql.DataFrame``
    :param column_1: Column on left dataframe.
    :type column_1: ``str``
    :param column_2: Column on right dataframe.
    :type column_2: ``str``
    :param type: Join type.
    :type type: ``str``
    :return: Joined dataframe.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df_1.join(df_2.withColumnRenamed(column_2, column_1), column_1, type)


def query_spark_sql(sql_context: CONTEXT, query: str) -> SDF:
    """Run SQL query using a Spark SQL context.
    
    :param sql_context: Pyspark SQL context used to run query.
    :type sql_context: ``pyspark.SQLContext``
    :param query: SQL query.
    :type query: ``str``
    :return: Pyspark DataFrame with query output.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return sql_context.sql(query)


def select_columns(df: SDF, *columns: str) -> SDF:
    """Select columns of pyspark dataframe.

    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param columns: Columns to be selected.
    :type columns: ``str``
    :return: Filtered spark dataframe.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.select(*columns)


def spark_to_pandas(df: SDF) -> DF:
    """Query spark dataframe getting pandas dataframe.

    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :return: Pandas dataframe with the data.
    :rtype: ``pandas.DataFrame``
    """
    return df.toPandas()


def weighted_mean(df: SDF, values_column: str, weight_column: str) -> float:
    """Takes weighted mean on `values_column` by `weighted_column`.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param values_column: Column to take weighted mean.
    :type values_column: ``str``
    :param weight_column: Column with weight.
    :type weight_column: ``str``
    :return: Weighted mean.
    :rtype: ``float``
    """
    # noinspection PyUnresolvedReferences
    return df.select(f.sum(df[values_column] * df[weight_column]) / f.sum(df[weight_column])).collect()[0][0]
