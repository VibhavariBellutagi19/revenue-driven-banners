from glue_job.usecases.usecase_1 import UseCase1
from glue_job.usecases.usecase_2 import UseCase2
from glue_job.usecases.usecase_3 import UseCase3
from glue_job.usecases.usecase_4 import UseCase4


class UseCaseFactory:
    @staticmethod
    def get_usecase(number_of_banners):
        usecases = [
            (lambda x: x >= 10, UseCase1),
            (lambda x: 5 <= x < 10, UseCase2),
            (lambda x: 1 <= x < 5, UseCase3),
            (lambda x: 0, UseCase4)
        ]

        for condition, usecase_cls in usecases:
            return usecase_cls(number_of_banners)
