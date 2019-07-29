from django.db import models
from .models import Sith as SithModel, Planet as PlanetModel
from .models import Recruit as RecruitModel, Question as QuestionModel
from .models import Answer as AnswerModel
from django.core.exceptions import ValidationError
import smtplib


class Mail():
    def __init__(self, mail, password):
        self.mail = mail
        self.smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtpObj.starttls()
        self.smtpObj.login(mail, password)

    def send(self, to_addr, msg):
        return self.smtpObj.sendmail(from_addr=self.mail, msg=msg, to_addrs=[to_addr])

    def close(self):
        self.smtpObj.close()


class DB:
    def __init__(self):
        self.db = models.Model.objects

    def get_all(self):
        return self.db.all()

    def get_by_id(self, id):
        return self.db.get(id=id)

    def get_values(self, column_name):
        value_pairs = self.get_all().values(column_name)
        values = []
        for value_pair in value_pairs:
            values.append(value_pair[column_name])
        return values


class PlanetDB(DB):
    def __init__(self):
        self.db = PlanetModel.objects

    def get_by_name(self, name):
        return self.db.get(name=name)


class SithDB(DB):
    def __init__(self):
        self.db = SithModel.objects

    def add_hand(self, sith):
        if sith.hands_count + 1 > sith.max_hands:
            raise ValidationError('Too much hands')
        sith.hands_count += 1
        sith.save()


class AnswerDB(DB):
    def __init__(self):
        self.db = AnswerModel.objects

    def add(self, answers, owner):
        for answer in answers.values():
            self.db.create(text=answer, owner=owner)


class QuestionDB(DB):
    def __init__(self):
        self.db = QuestionModel.objects


class RecruitDB(DB):
    def __init__(self):
        self.db = RecruitModel.objects

    def add(self, name, planet, age, email):
        try:
            recruit = RecruitModel(name=name, planet=planet, age=age, email=email)
            recruit.full_clean()
            recruit.save()
            return recruit
        except ValidationError as err:
            raise err