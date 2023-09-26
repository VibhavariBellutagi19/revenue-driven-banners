from usecase_1 import UseCase1
from usecase_2 import UseCase2
from usecase_3 import UseCase3
from usecase_4 import UseCase4


class UseCaseFactory:
    @staticmethod
    def get_usecase(number_of_banners: int):
        usecases = [
            (lambda x: x >= 10, UseCase1),
            (lambda x: 5 <= x < 10, UseCase2),
            (lambda x: 1 <= x < 5, UseCase3),
            (lambda x: x == 0, UseCase4)
        ]

        for condition, usecase_cls in usecases:
            if condition(number_of_banners):
                return usecase_cls(number_of_banners)
