from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.db.models import F
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# 手写生成view方法


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    # 手写template
    # template = loader.get_template("polls/index.html")
    # return HttpResponse(template.render(context, request))

    # render快捷方法
    return render(request, "polls/index.html", context)

    # output = ", ".join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)


def detail(request, question_id):
    # try:
    #   question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #   raise Http404("Question does not exist")

    # get_object_or_404 剩略try except
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(
            pk=request.POST["choice"])  # html <inpurt name="choice">
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    # else对应的except，没有异常走这里
    else:
        selected_choice.votes = F("votes") + 1  # F转成字段
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # reverse() 根据urls path定义生成路由字符串
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# 定义modelView类，简化代码
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
