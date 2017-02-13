from django import forms
from .models import Question,Answer
from pagedown.widgets import PagedownWidget
class QuestionForm(forms.ModelForm):
    content=forms.CharField(widget=PagedownWidget)
    class Meta:
        model=Question
        fields=[
        "title",
        "content",
         ]

class AnswerForm(forms.ModelForm):
   content_type = forms.CharField(widget=forms.HiddenInput)
   object_id = forms.IntegerField(widget=forms.HiddenInput)
   content = forms.CharField(widget=PagedownWidget)
   class Meta:
       model=Answer
       fields=[
           "content",
       ]




