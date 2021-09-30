import json

from importlib import import_module
from django.conf import settings

from .engine_module import PsychicListJsonEncoder, PsychicList, Psychic, User, UserJsonEncoder

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


class AbstractStorage:

    def __call__(self, session_key):
        self.session_key = session_key

    def save(self, session_key, obj: object):
        raise NotImplementedError

    def load(self, session_key) -> object:
        raise NotImplementedError


class PsychicAbstractStorage(AbstractStorage):

    def save(self, session_key, obj: PsychicList):
        raise NotImplementedError

    def load(self, session_key) -> PsychicList:
        raise NotImplementedError

    def save_user(self, session_key, user: User):
        raise NotImplementedError

    def load_user(self, session_key) -> User:
        raise NotImplementedError


class PsychicSessionStorage(PsychicAbstractStorage):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store = SessionStore(session_key=None)

    def save(self, session_key, obj: PsychicList) -> None:
        self.store['psychic_list'] = json.dumps(obj, cls=PsychicListJsonEncoder)
        # self.store.save()

    def save_user(self, session_key, user: User) -> None:
        self.store['user_numbers'] = json.dumps(user, cls=UserJsonEncoder)
        # self.store.save()

    def load(self, session_key) -> PsychicList():
        list_json = json.loads(self.store['psychic_list'])
        the_list_psychics = PsychicList()
        for psy in list_json:
            psy = Psychic(predict_number=psy['predict_number'], success=psy['success'])
            the_list_psychics.add_psychics_to_list(psy)
        return the_list_psychics

    def load_user(self, session_key) -> User():
        list_json = json.loads(self.store['user_numbers'])
        gamer = User(user_number=list_json['user_number'])
        return gamer


class StorageFactory:

    @staticmethod
    def create_storage() -> AbstractStorage:
        assert issubclass(settings.STORAGE, AbstractStorage)
        return settings.STORAGE()


storage = PsychicSessionStorage()
