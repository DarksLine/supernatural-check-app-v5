from random import randint
import json


class User:
    __slots__ = ['user_number']

    def __init__(self, user_number: list = []) -> None:
        self.user_number = user_number

    def get_user_number(self, number):
        self.user_number.append(number)


class Psychic:
    __slots__ = ['predict_number', 'success']

    def __init__(self, predict_number: list = [], success: int = 0) -> None:
        self.predict_number = predict_number
        self.success = success

    def try_predict_number(self):
        number = randint(10, 99)
        self.predict_number.append(number)

    def add_success(self):
        self.success += 1

    def result_predict(self, user_number: int) -> None:
        if self.predict_number[-1] == user_number:
            self.add_success()


class PsychicList:

    def __init__(self) -> None:
        self.list_psychics: list(Psychic) = []

    def create_list_psychics(self, count_psy: int) -> None:
        for i in range(count_psy):
            psy = Psychic()
            self.list_psychics.append(psy)

    def add_psychics_to_list(self, obj: Psychic) -> None:
        self.list_psychics.append(obj)


class UserJsonEncoder(json.JSONEncoder):
    def default(self, obj: User):
        if isinstance(obj, User):
            return {
                'user_number': obj.user_number,
            }

        return super().default(obj)


class PsychicListJsonEncoder(json.JSONEncoder):
    def default(self, obj: PsychicList):
        if isinstance(obj, PsychicList):
            list_json = []

            for el in obj.list_psychics:
                list_json.append({
                    'predict_number': el.predict_number,
                    'success': el.success
                })
            return list_json

        return super().default(obj)








# class PsyList:
#     # Создать и вернуть список экстрасенсов
#     @classmethod
#     def create_psychic(cls, count_psychics):
#         list_psychics = []
#         for person in range(count_psychics):
#             list_psychics.append(Psychic())
#
#         return list_psychics
#
#     # Получить результаты предположений
#     @classmethod
#     def get_predict_psychics(cls, list_psychic):
#         for obj in list_psychic:
#             obj.predict_number()




# Класс-миксин для подсчета процента достоверности предсказаний
class PercentMixin:
    @classmethod
    def percent(cls, request, predict, mind):
        success = request.session["success"]
        for element in predict:
            if predict.get(element) == mind:
                success[element] = success[element] + 1

        percent = {'num1': 0, 'num2': 0, 'num3': 0}
        for element in percent:
            percent[element] = int((success.get(element) / request.session["iter"]) * 100)
        request.session["success"] = success
        return percent