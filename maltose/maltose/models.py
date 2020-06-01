import datetime

from django.conf import settings
from django.db import models
from django.core.files import File


class ModelSerializationMixin:
    @staticmethod
    def get_exclude():
        return []

    @staticmethod
    def _to_dict(
        model,
        fields=None,
        exclude=None,
        relation=False,
        relation_data=None,
        raw_data=False,
        **kwargs
    ):
        """
        将Model对象序列化

        * int, str, float等对象正常解析
        * DateTimeField解析为2018-12-01 00:00:00格式,
        * DateField解析为2018-12-01格式
        * FileField, ImageField等解析为路径字符串

        :param self: Model 需要序列化的对象
        :param fields: str[] 需要序列化的字段名, 不给值时默认序列化所有字段
        :param exclude: str[] 不需要序列化的字段名
        :param relation: Boolean 为真时序列化关系字段
        :param relation_data: Boolean 为假时仅序列化关系字段的id, 默认值等于relation
        :param kwargs: 需要额外序列化的变量
        :return: dict
        """
        if model is None:
            return None

        result, exclude = dict(), exclude if exclude else model.get_exclude()
        relation_data = relation_data if relation_data is not None else relation

        def _get_fields(self, fields=None):
            if fields is None:
                for field in self._meta.get_fields():
                    yield field
            else:
                for field_name in fields:
                    yield self._meta.get_field(field_name)

        for field in _get_fields(model, fields):
            if field.name in exclude:
                continue
            if field.many_to_many:
                if not relation:
                    continue
                if isinstance(field, models.ManyToManyRel):
                    if field.related_name is None:
                        querySet = getattr(model, field.name + "_set").all()
                    else:
                        querySet = getattr(model, field.related_name).all()
                else:
                    querySet = getattr(model, field.name).all()
                if relation_data:
                    result[field.name] = [model._to_dict(each) for each in querySet]
                else:
                    result[field.name] = [each.id for each in querySet]
            elif field.one_to_many:
                if not relation:
                    continue
                if field.related_name is None:
                    querySet = getattr(model, field.name + "_set").all()
                else:
                    querySet = getattr(model, field.related_name).all()
                if relation_data:
                    result[field.name] = [model._to_dict(each) for each in querySet]
                else:
                    result[field.name] = [each.id for each in querySet]
            elif field.one_to_one or field.many_to_one:
                if not relation:
                    continue
                if relation_data:
                    result[field.name] = model._to_dict(getattr(model, field.name))
                else:
                    result[field.name] = getattr(model, field.name + "_id")
            else:
                result[field.name] = getattr(model, field.name)

            if not raw_data:
                if isinstance(result[field.name], datetime.date):
                    result[field.name] = result[field.name].strftime("%Y-%m-%d")
                elif isinstance(result[field.name], datetime.datetime):
                    result[field.name] = result[field.name].strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                elif isinstance(result[field.name], (File,)):
                    result[field.name] = settings.MEDIA_URL + str(result[field.name])

        result.update(**kwargs)
        return result

    def to_dict(
        self,
        *,
        fields=None,
        exclude=None,
        relation=False,
        relation_data=None,
        raw_data=False,
        **kwargs
    ):
        return self._to_dict(
            self,
            fields=fields,
            exclude=exclude,
            relation=relation,
            relation_data=relation_data,
            raw_data=raw_data,
            **kwargs
        )
