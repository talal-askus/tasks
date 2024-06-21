from django.shortcuts import render,get_object_or_404
from .models import Question
from django.http import Http404


# Create your views here.
from django.http import HttpResponse


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = { "latest_question_list": latest_question_list}
    return render(request,"polls/index.html",context)

def details(request, question_id):
    question = get_object_or_404(Question, pk= question_id)
    return render(request, "polls/detail.html", {"question":question})

def result(request, question_id):

    response= "You are Looking at the Results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

