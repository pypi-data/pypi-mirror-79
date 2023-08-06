from typing import List
from pyspark.sql import SparkSession # pylint: disable = unused-import
from databricksbundle.spark.SparkSessionLazy import SparkSessionLazy
from databricksbundle.spark.config.ConfiguratorInterface import ConfiguratorInterface

class DatabricksSessionFactory:

    def __init__(
        self,
        configurators: List[ConfiguratorInterface],
    ):
        self.__configurators = configurators

    def create(self) -> SparkSessionLazy:
        spark = globals()['spark'] # type: SparkSession

        for configurator in self.__configurators:
            configurator.configure(spark)

        globals()['spark'] = spark

        return SparkSessionLazy(lambda: spark)
