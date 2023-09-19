from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from pyspark.sql import DataFrame, SparkSession


@dataclass
class ActionDataFrames:
    clicks_df: Union[DataFrame, None] = None
    conversions_df: Union[DataFrame, None] = None
    impressions_df: Union[DataFrame, None] = None


class UseCase(ABC):
    @abstractmethod
    def compute_use_case(self, spark: SparkSession, dataframes: ActionDataFrames) -> DataFrame:
        pass