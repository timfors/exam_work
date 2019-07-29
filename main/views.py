from django.shortcuts import render, redirect
from django.db import IntegrityError, DataError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .essences import *


# Create your views here.


def index(request):
    return render(request, "index.html")


def recruit_register(request):
    recruit_db = RecruitDB()
    planet_db = PlanetDB()
    all_planets = planet_db.get_all().order_by('name')
    if request.method == 'GET':
        return render(request, "recruit.html", {'planets': all_planets})
    elif request.method == 'POST':
        post_data = get_form_values(request, ["name", "planet", "age", "email"])
        try:
            planet = planet_db.get_by_name(post_data["planet"])
            new_recruit = recruit_db.add(name=post_data["name"], planet=planet,
                                         age=post_data["age"], email=post_data["email"])
            request.session["id"] = new_recruit.id
            return redirect("/recruit/test")
        except IntegrityError:
            return render(request, "recruit.html", {'planets': all_planets,
                                                    'errors': 'Email уже существует'})
        except ObjectDoesNotExist:
            return render(request, "recruit.html",
                          {'planets': all_planets, 'errors': 'Планета отсутсвует в базе'})
        except ValidationError as err:
            return render(request, "recruit.html", {'planets': all_planets, 'errors': err})


def test_recruit(request):
    question_db = QuestionDB()
    all_questions = question_db.get_all().order_by('id')
    if request.method == 'GET':
        if request.session["id"]:
            return render(request, "test.html", {'questions': all_questions})
        else:
            return redirect('/recruit')
    elif request.method == 'POST':
        try:
            recruit_db = RecruitDB()
            answer_db = AnswerDB()
            questions_id = question_db.get_values('id')
            recruit_id = request.session["id"]
            recruit = recruit_db.get_by_id(recruit_id)
            post_data = get_form_values(request, questions_id)
            answer_db.add(post_data, recruit)
            request.session["id"] = None
            return redirect('/')
        except ObjectDoesNotExist as err:
            return render(request, "test.html", {'questions': all_questions,
                                                 'error': err.__context__})
        except ValidationError as err:
            return render(request, "test.html", {'questions': all_questions,
                                                 'error': err.__context__})


def sith(request):
    sith_db = SithDB()
    all_siths = sith_db.get_all().order_by('name')
    siths_with_2_or_more_hands = sith_db.get_all().filter(
        hands_count__gte=2).order_by('hands_count')
    return render(request, "sith.html", {'siths': all_siths,
                                         'siths_with_2_or_more_hands': siths_with_2_or_more_hands})


def all_recruits(request, sithid):
    try:
        sith_db = SithDB()
        sith_db.get_by_id(sithid)
        recruit_db = RecruitDB()
        all_rec = recruit_db.get_all().order_by('name')
        return render(request, 'all_recruits.html', {'recruits': all_rec})
    except ObjectDoesNotExist:
        return redirect('/sith')


def recruit_answer(request, sithid, recruitid):
    try:
        question_db = QuestionDB()
        all_questions = question_db.get_all().order_by('id')
        answer_db = AnswerDB()
        recruit_db = RecruitDB()
        recruit = recruit_db.get_by_id(recruitid)
        answers = answer_db.get_all().filter(owner=recruit).order_by('id')
        if request.method == 'GET':
            return render(request, 'recruit_answer.html', {'answers': answers, 'questions': all_questions})
        elif request.method == 'POST':
            add_hand(sithid, recruitid)
            return redirect('/sith/%s' % sithid)
    except ValidationError as err:
        return render(request, 'recruit_answer.html', {'answers': answers, 'questions': all_questions,
                                                       'error': err})
    except DataError as err:
        return render(request, 'recruit_answer.html', {'answers': answers, 'questions': all_questions,
                                                       'error': err})
    except ObjectDoesNotExist:
        return redirect('/sith/%s' % sithid)


def add_hand(sithid, recruitid):
    try:
        sith_db = SithDB()
        sith = sith_db.get_by_id(sithid)
        sith_db.add_hand(sith)
        recruit_db = RecruitDB()
        recruit = recruit_db.get_by_id(recruitid)
        mail = Mail('grand.sith.sender@gmail.com', 'grand.sith1')
        mail.send(msg='YOU ARE HAND NOW!', to_addr=recruit.email)
        mail.close()
        recruit.delete()
        return redirect('/sith/%s' % sithid)
    except ValidationError:
        raise ValidationError('Too much hands')
    except DataError:
        raise DataError('Something wrong with mail')


def get_form_values(request, keys):
    values = {}
    for key in keys:
        values[key] = request.POST.get(str(key))
    return values
