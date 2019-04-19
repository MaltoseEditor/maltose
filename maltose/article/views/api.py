import json

from django.http.response import JsonResponse
from django.http.request import QueryDict
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.conf import settings
from django.views import View

from maltose.article import render as markdown
from maltose.article.models import Article, Tag, Corpus, Reference, Image

__all__ = [
    'ArticleView',
    'TagView',
    'CorpusView',
    'ReferenceView',
    'ImageView',
    'RenderView',
]


def restful(message="", error=None, data=None, status=200, **kwargs):
    """
    :param message: 交付与前端, 给用户看的信息
    :param error: 用于调试时阅读的错误信息
    :param data: 被请求的数据
    :param status: HTTP状态码, 详见 https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status
    :param kwargs: JsonResponse的其他参数
    :return:
    """
    return JsonResponse({"message": message, "error": error, "data": data}, status=status, **kwargs)


class LoginRequiredView(View):

    def dispatch(self, request, *args, **kwargs):
        if settings.DEBUG or request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return restful(message='未登陆', error='没有携带Cookies或Cookies失效', status=403)


class ModelApiView(LoginRequiredView):
    """
    对模型进行操作的Api视图
    """
    Model = None  # 此Api操作的模型
    Form = None  # 用于post, put, patch方法中处理数据的Form表单
    list_exclude = None  # 排除(读取全部数据/创建数据)时的部分字段, 需要一个可迭代对象 例如 ('password', 'email')
    inherit_method_list = tuple()  # 指定继承哪些操作方法, 需要一个可迭代对象 例如 ('get', 'post', 'delete')

    def __init__(self, **kwargs):
        for each in self.inherit_method_list:
            setattr(self, each, getattr(self, '_' + each))
        super().__init__(**kwargs)
        if self.Form is None:
            class DefaultForm(ModelForm):
                class Meta:
                    model = self.Model
                    fields = '__all__'

            self.Form = DefaultForm

    def dispatch(self, request, *args, **kwargs):
        request.json = None
        if request.content_type == 'application/json':
            request.json = json.loads(request.body)
        elif request.method != 'POST':  # 对于非json格式的非post请求, 也进行解析
            request.POST = QueryDict(request.body)
        self.data = request.POST if request.json is None else request.json
        # 捕获所有请求中的Model.DoesNotExist, 统一回复
        try:
            return super().dispatch(request, *args, **kwargs)
        except self.Model.DoesNotExist:
            return restful("请求的数据不存在", status=404)

    def _get(self, request):
        if request.GET.get('id') is not None:
            obj = self.Model.objects.get(id=request.GET.get('id'))
            return restful(data=obj.to_dict(relation=True))

        return restful(data=[
            obj.to_dict(exclude=self.list_exclude)
            for obj in self.Model.objects.all()
        ])

    def _post(self, request):
        form = self.Form(self.data, request.FILES)
        if form.is_valid():
            obj = form.save(commit=True)
            return restful("新建成功", data=obj.to_dict())
        return restful(error=form.errors, status=400)

    def _put(self, request):
        obj = self.Model.objects.get(id=request.GET.get('id'))
        form = self.Form(self.data, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            return restful("保存成功", data=obj.to_dict())
        return restful(error=form.errors, status=400)

    def _patch(self, request):
        obj = self.Model.objects.get(id=request.GET.get('id'))
        init_data = model_to_dict(obj)
        init_data.update(self.data)
        form = self.Form(init_data, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            return restful("更改成功", data=obj.to_dict())
        return restful(error=form.errors, status=400)

    def _delete(self, request):
        obj = self.Model.objects.get(id=request.GET.get('id'))
        try:
            obj.delete()
        except Exception as e:
            return restful(error=e, status=400)
        return restful("删除成功")


class ArticleView(ModelApiView):
    """
    对文章的操作
    """
    Model = Article
    list_exclude = ('source', 'body')
    inherit_method_list = ('post', 'put', 'delete', 'patch')

    def get(self, request):
        if request.GET.get('id') is not None:
            obj = self.Model.objects.get(id=request.GET.get('id'))
            return restful(data=obj.to_dict(relation=True))

        return restful(data=[
            obj.to_dict(exclude=self.list_exclude)
            for obj in self.Model.objects.all().order_by('-create_time')
        ])


class TagView(ModelApiView):
    """
    对标签的操作
    """
    Model = Tag
    inherit_method_list = ['get', 'post', 'delete']


class CorpusView(ModelApiView):
    """
    对文集的操作
    """
    Model = Corpus
    inherit_method_list = ['get', 'post', 'delete']


class ReferenceView(ModelApiView):
    """
    对引用链接的操作
    """
    Model = Reference
    inherit_method_list = ['post', 'patch', 'delete']


class ImageView(ModelApiView):
    """
    对图片的操作
    """
    Model = Image
    inherit_method_list = ['post', 'delete']


class RenderView(View):
    """
    使用Python进行渲染的接口
    """

    def post(self, request):
        if request.content_type == 'application/json':
            source = json.loads(request.body).get('source')
        else:
            source = request.POST.get('source')
        if source is not None:
            return restful(data={"result": markdown(source)})
        return restful("未接收到source", {"request.body": str(request.body)}, status=400)
