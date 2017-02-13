from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from markdown_deux import  markdown
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class Question(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    title=models.CharField(max_length=120)
    slug=models.SlugField(unique=True)
    content=models.TextField()
    updated=models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)


    def __str__(self):
        return self.title
    def get_absolute_urls(self):
        return reverse("forum:question_detail",kwargs={"slug":self.slug})

    class Meta:
       ordering=["-timestamp","-updated"]

    def get_markdown(self):
        content=self.content
        markdown_text=markdown(content)
        return mark_safe(markdown_text)

def create_slug(instance,new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    qs=Question.objects.filter(slug=slug).order_by("-id")
    exists=qs.exists()
    if exists:
        new_slug="%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)

pre_save.connect(pre_save_post_receiver,sender=Question)

class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    upvote = models.ManyToManyField(User, related_name='upvote')
    downvote = models.ManyToManyField(User, related_name='downvote')
    timestamp = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.user.username

    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.upvote.count()

    @property
    def total_dislikes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.downvote.count()
