from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from pyspark.sql import DataFrame, SparkSession


class UseCase(ABC):
    @abstractmethod
    def compute_use_case(self, spark: SparkSession) -> DataFrame:
        pass