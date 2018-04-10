from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token, ensure_csrf_cookie

from .models import Person, Poll, Question, Choice


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


def polls_list(request):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})
    else:
        all_polls = Poll.objects.all().order_by('-pub_date')
        paginator = Paginator(all_polls, 5)
        page = request.GET.get('page')
        try:
            polls = paginator.page(page)
        except PageNotAnInteger:
            polls = paginator.page(1)
        except EmptyPage:
            polls = paginator.page(paginator.num_pages)
        return render(request, 'polls/polls_list.html', {'polls': polls})


def poll(request, poll_id):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})
    else:
        try:
            poll = Poll.objects.get(pk=poll_id)
            questions = Question.objects.filter(poll_id=poll_id)
            is_finished = False
            # user = Person.objects.get(id=32)
            finished_poll = Poll.objects.filter(pk=poll_id, user=request.user)
            if finished_poll.count() > 0:
                poll_questions = Question.objects.filter(poll_id=finished_poll.first().pk)
                answered_questions_number = 0
                for question in poll_questions:
                    answered_questions = Question.objects.filter(id=question.id, user=request.user)
                    if answered_questions.count() > 0:
                        answered_questions_number += 1
                if answered_questions_number == poll_questions.count():
                    is_finished = True
        except Poll.DoesNotExist:
            raise Http404("Not found")
        return render(
            request,
            'polls/poll_page.html',
            {
                'poll': poll,
                'questions': questions,
                'is_finished': is_finished,
            }
        )


@csrf_exempt
def choose(request):
    # person = Person.objects.get(id=32)
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})
    else:
        if request.method == 'POST':
            if 'choice_id' in request.POST:
                choice_id = request.POST['choice_id']
                person = request.user
                if choice_id:
                    choice = Choice.objects.filter(id=int(choice_id)).first()
                    question = Question.objects.filter(id=choice.question_id, user=person)
                    if question.count() == 0:
                        votes_for_choice = choice.choice_user_count + 1
                        choice.choice_user_count = votes_for_choice
                        question = Question.objects.get(id=choice.question_id)
                        question.question_user_count += 1
                        poll = Poll.objects.get(id=question.poll_id)
                        question.user = person
                        poll.user.add(person)
                        question.save()
                        choice.save()
                        all_choices = Choice.objects.filter(question_id=question.id)
                        for choice in all_choices:
                            choice.save()
                        poll.save()
                        is_poll_finished(question.id, person.id)
                        return HttpResponse(votes_for_choice)
                    else:
                        return HttpResponse({})


def is_poll_finished(question_id, person_id):
    person = Person.objects.get(id=person_id)
    question = Question.objects.get(id=question_id)
    poll = Poll.objects.get(id=question.poll_id, user=person)
    all_questions = Question.objects.filter(poll_id=poll.id)
    answered_questions_number = 0
    for question in all_questions:
        answered_questions = Question.objects.filter(id=question.id, user=person)
        if answered_questions.count() > 0:
            answered_questions_number += 1
    if answered_questions_number == all_questions.count():
        poll.is_finished = True
        poll.save()






