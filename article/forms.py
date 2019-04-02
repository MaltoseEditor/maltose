from django.forms import ModelForm

from .models import *


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class CorpusForm(ModelForm):
    class Meta:
        model = Corpus
        fields = '__all__'


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        fields = '__all__'


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
