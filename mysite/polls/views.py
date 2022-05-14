# from curses.ascii import HT
# from django.shortcuts import render, get_object_or_404
# from urllib import response
# from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.template import loader
# from .models import Question, Choice
# from django.urls import reverse


# # Create your views here.
# # def index(request):
# #     # /// return HttpResponse("Hello, World!")
# #     latest_question_list = Question.objects.order_by('-pub_date')[:5]
# #     # /// output = ', '.join([q.question_text for q in latest_question_list])
# #     # /// return HttpResponse(output)
# #     template = loader.get_template('polls/index.html')
# #     context = {'latest_question_list':latest_question_list,}
# #     return HttpResponse(template.render(context, request))

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list':latest_question_list}
#     return render(request, 'polls/index.html', context)


# # def detail(request, question_id):
# #     # /// return HttpResponse("You are looking at question %s." %question_id)
# #     try:
# #         question = Question.objects.get(pk = question_id)
# #     except Question.DoesNotExist:
# #         raise Http404("Question does not exist")
# #     return render(request, 'polls/detail.html', {'question':question})
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     # response = "You are looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, 'polls/results.html', {'question':question})


# def vote(request, question_id):
#     # return HttpResponse("You are voting on question %s." % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk = request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/detail.html',{
#             'question':question,
#             'error_message':"You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

from re import template
from typing import Generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question

class IndexView(generic.ListView):
    template_name =  'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # return HttpResponse("You are voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question':question,
            'error_message':"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


