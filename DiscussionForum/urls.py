from django.conf.urls import url
from DiscussionForum import views
urlpatterns = [
    url(r'^$', views.question_list, name="question_list"),
    url(r'^create/$',views.question_create,name="question_create"),
    url(r'^activity/$',views.user_activity,name="activity"),
    url(r'^(?P<slug>[\w-]+)/$',views.question_detail,name="question_detail"),
    url(r'^(?P<slug>[\w-]+)/upvote/$',views.upvote, name="upvote"),
    url(r'^(?P<slug>[\w-]+)/downvote/$', views.downvote, name="downvote"),
    url(r'^(?P<slug>[\w-]+)/edit/$',views.question_update,name="question_update"),
    url(r'^(?P<slug>[\w-]+)/delete/$',views.question_delete,name="question_delete"),
]