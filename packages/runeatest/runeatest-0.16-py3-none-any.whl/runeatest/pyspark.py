import json
import pyspark


def get_dbutils(spark):
    try:
        from pyspark.dbutils import DBUtils

        dbutils = DBUtils(spark)
    except ImportError:
        import IPython

        dbutils = IPython.get_ipython().user_ns["dbutils"]
    return dbutils


def get_context():

    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession

    spark = SparkSession.builder.appName("runeatest").getOrCreate()
    dbutils = get_dbutils(spark)
    context = json.loads(
        dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson()
    )
    return context
