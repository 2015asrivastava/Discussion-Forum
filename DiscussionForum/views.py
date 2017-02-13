from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .forms import AnswerForm,QuestionForm
from .models import Answer,Question
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.db.models import F
from django.urls import reverse
from  django.db.models import Q
from django.db.models import Count
from  django.contrib.auth.decorators import login_required
import json
# Create your views here.

def question_create(request):
    current_user = request.user
    if request.user.is_authenticated or request.user.is_superuser:
        username=request.user.username
        form=QuestionForm(request.POST or None)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_urls())

        context_dict={
            "form":form,
        }

        return  render(request,"question_create.html",context_dict)
    else:
        raise Http404


def question_detail(request,slug):

    question = get_object_or_404(Question, slug=slug)


    content_type=ContentType.objects.get_for_model(Question)
    object_id=question.id
    initial_data = {
        "content_type": content_type,
        "object_id": question.id,
    }
    form=AnswerForm(request.POST or None,initial=initial_data)
    user=request.user
    if form.is_valid():
        content_type=ContentType.objects.get_for_model(Question)

        object_id1=form.cleaned_data.get("object_id")

        content_data=form.cleaned_data.get("content")

        new_answer,created=Answer.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id1,
            content=content_data,

        )

        return HttpResponseRedirect(new_answer.content_object.get_absolute_urls())
    answers=Answer.objects.filter(content_type=content_type,object_id=object_id).annotate(upvote_count=Count("upvote")).order_by("-upvote_count")

    

    context_dict={

        "question":question,
        "answers":answers,
        "form":form,


    }

    return render(request, "question_detail.html",context_dict)

def question_list(request):
    question_list=Question.objects.all()
    no_search=None
    query = request.GET.get("q")
    if query:
        question_list=question_list.filter(Q(title__icontains=query)|
                                           Q(content__icontains=query)|
                                           Q(user__first_name__icontains=query)|
                                           Q(user__last_name__icontains=query)
                                           ).distinct()
        if(question_list.count()==0):
            no_search="Sorry! No content matches your criteria.Please try some different keywords"



    paginator=Paginator(question_list,5)
    page = request.GET.get('page')
    try:
        question_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        question_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        question_list = paginator.page(paginator.num_pages)
    context={
         "question_list":question_list,
          "no_search":no_search

    }
    return render(request,"question_list.html",context)


def upvote(request,slug):
    if request.user.is_authenticated or request.user.is_superuser:

        if request.method == 'GET':
            is_downvote_exits=False
            message=None
            user = request.user
            content_type = ContentType.objects.get_for_model(Question)

            question = get_object_or_404(Question, slug=slug)
            question_id=question.id
            content_data=request.GET['answer_id']
            answer_id=request.GET['answer_id']
            answered=Answer.objects.get(
                id=answer_id,
                object_id=question_id,
             )
            xyz=answered.content
            new_answer= Answer.objects.get(
                # user=request.user,
                content_type=content_type,
                object_id=question_id,
                content=xyz,
             )

            if new_answer.upvote.filter(id=user.id).exists():
                like = new_answer.total_likes
                dislike = new_answer.total_dislikes
                message="You had already liked this"
            else:
                if new_answer.downvote.filter(id=user.id).exists() :
                    new_answer.downvote.remove(user)
                    new_answer.upvote.add(user)
                    is_downvote_exits=True
                    like=new_answer.total_likes
                    dislike=new_answer.total_dislikes
                else:
                    new_answer.upvote.add(user)
                    like = new_answer.total_likes
                    dislike=new_answer.total_dislikes
        context_dict={
            "likes":like,
             "dislikes":dislike,
             "is_downvote_exists":is_downvote_exits,
             "message":message,
        }
        return HttpResponse(json.dumps(context_dict),content_type="application/json")
    else:
        raise Http404


def downvote(request, slug):
    if request.user.is_authenticated or request.user.is_superuser:

        if request.method == 'GET':
            is_upvote_exits=False
            message = None
            user = request.user
            content_type = ContentType.objects.get_for_model(Question)
            question = get_object_or_404(Question, slug=slug)
            question_id = question.id
            content_data = request.GET['answer_id']
            answer_id = request.GET['answer_id']
            answered = Answer.objects.get(
                id=answer_id,
                object_id=question_id,
            )
            xyz = answered.content
            new_answer = Answer.objects.get(
                # user=request.user,
                content_type=content_type,
                object_id=question_id,
                content=xyz,
            )

            if new_answer.downvote.filter(id=user.id).exists():
                like = new_answer.total_likes
                dislike = new_answer.total_dislikes
                message="You had already disliked this"
            else:
                if new_answer.upvote.filter(id=user.id).exists():
                    new_answer.upvote.remove(user)
                    new_answer.downvote.add(user)
                    is_upvote_exits = True
                    like = new_answer.total_likes
                    dislike = new_answer.total_dislikes
                else:
                    new_answer.downvote.add(user)
                    like = new_answer.total_likes
                    dislike = new_answer.total_dislikes
            context_dict = {
                "likes": like,
                "dislikes": dislike,
                "is_upvote_exists": is_upvote_exits,
                "message":message,
            }
        return HttpResponse(json.dumps(context_dict), content_type="application/json")
    else:
        raise Http404

def question_update(request,slug=None):
    if request.user.is_authenticated or request.user.is_superuser:
        user=request.user
        if(user.id==1):
            instance = get_object_or_404(Question, slug=slug)
        else:
          instance = get_object_or_404(Question, slug=slug,user_id=user.id)
        form = QuestionForm(request.POST or None,request.FILES or None,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Question successfully updated")
            return HttpResponseRedirect(instance.get_absolute_urls())
        context = {
            "form":form,
            "instance":instance,
        }
        return render(request, "question_create.html", context)
    else:
        raise Http404

def question_delete(request,slug=None):
    if request.user.is_authenticated or request.user.is_superuser:
        user=request.user
        if user.id==1:
            instance = get_object_or_404(Question, slug=slug)
            messages.success(request, "Question successfully deleted")
        else:
          instance = get_object_or_404(Question, slug=slug,user_id=user.id)
          messages.success(request,"Question successfully deleted")
        instance.delete()
        return redirect("forum:question_list")
    else:
        raise Http404

def user_activity(request):
    user=request.user
    questions=Question.objects.all()
    question_list=questions.filter(user_id=user.id)
    paginator = Paginator(question_list, 5)
    page = request.GET.get('page')
    title="Questions Asked"
    try:
        question_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        question_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        question_list = paginator.page(paginator.num_pages)
    context_dict={
        "question_list":question_list,
        "title":title,
    }

    return render(request, "question_list.html", context_dict)