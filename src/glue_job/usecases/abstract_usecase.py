from abc import ABC, abstractmethod

from pyspark.sql import DataFrame, SparkSession


class UseCase(ABC):
    @abstractmethod
    def compute_use_case(self, spark: SparkSession) -> DataFrame:
        pass