import datetime
import json

from aiogram import types

import os

import django
from asgiref.sync import sync_to_async

from quiz.models import User, Survey

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot.settings")
django.setup()
# from config import db_user, db_pass, host
#
# db = Gino()
#
#
# class User(db.Model):
#     __tablename__ = "users"
#     id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
#     user_id = Column(BigInteger)
#     first_name = Column(String(50))
#     last_name = Column(String(50))
#     user_name = Column(String(50))
#     is_bot = Column(Boolean, unique=False, default=False)
#     referral = Column(Integer)
#     query: sql.Select
#
#
# class Survey(db.Model):
#     __tablename__ = "survey"
#
#     id = Column(Integer, Sequence("survey_id_seq"), primary_key=True)
#     user_id = Column(BigInteger)
#     answers = Column(String)
#     time_start = Column(TIMESTAMP)
#     time_finish = Column(TIMESTAMP)


class DBCommands:
    @sync_to_async
    def get_user(self, user_id) -> User:
        user = None
        try:
            user = User.objects.get(telegram_id=user_id)
        except User.DoesNotExist:
            pass
        return user

    async def add_new_user(self, referral=None) -> User:
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user is not None:
            return old_user
        new_user = User()
        new_user.telegram_id = user.id
        new_user.name = user.first_name
        new_user.last_name = user.last_name
        new_user.telegram_login = user.username
        if referral:
            new_user.referral = self.get_user(referral)
        await sync_to_async(new_user.save)()
        return new_user

    @sync_to_async
    def get_survey(self, survey_id) -> Survey:
        survey = None
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            pass
        return survey

    # async def add_or_update_survey(self, answer, is_last_answer = False) -> Survey:
    #     user = types.User.get_current()
    #     survey = await self.get_survey(user.id)
    #     answers = {}
    #     if survey:
    #         answers = json.loads(survey.answers)
    #     else:
    #         survey = Survey()
    #         survey.user_id = user.id
    #         survey.time_start = datetime.datetime.now()
    #     answers.update(answer)
    #     survey.answers = json.dumps(answers)
    #     if is_last_answer:
    #         survey.time_finish = datetime.datetime.now()
    #     if survey.id:
    #         await survey.update(answers=json.dumps(answers)).apply()
    #         if is_last_answer:
    #             await survey.update(time_finish = datetime.datetime.now()).apply()
    #     else:
    #         await survey.create()
    #     return survey

#
# async def create_db():
#     await db.set_bind(f"postgresql://{db_user}:{db_pass}@{host}/gino")
#     db.gino: GinoSchemaVisitor
#     await db.gino.drop_all()
#     await db.gino.create_all()