from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import requests
import json
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    return render(request, 'polls/detail.html', {'question': question})
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def testGH(request):
    return render(request, 'polls/testGH.html')

def testGHresult(request):
    gihubuser=request.POST['username']
    request.session['OurUser']=gihubuser
    yoko = requests.get('https://api.github.com/users/%s/repos' % request.session['OurUser'])

    contextGH = {}
    contextGH['repos'] = yoko.json()
    contextGH['usergit'] = gihubuser
    return render(request, 'polls/testGHresult.html', contextGH)

def OrganizationPage(request):
    codeauth=request.GET['code']
    payload = {'client_id': 'cdfbe6c5153b91acf782', 'client_secret': '196d6896116217b246d4e9aee4107aa389a39ea8', 'code': codeauth}
    yokaaa=requests.post('https://github.com/login/oauth/access_token?', params=payload).text.split("&")
    yokaa = yokaaa[0].split("=")
    yoki = yokaa[1]
    yoka = requests.get('https://api.github.com/user/orgs?access_token=' + yoki)
    contextGH = {'usergit' : request.session.get('OurUser'),
    'codeauth' : codeauth,
    'yoka' : yoka.json()}

    yoku = requests.get('https://api.github.com/orgs/vitoisanorganization/members')
    contextGH['yoku'] = yoku
    return render(request, 'polls/OrganizationPage.html',contextGH)
