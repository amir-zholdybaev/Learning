from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework import generics

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password'
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)


class UserAPIList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""
    ModelSerializer.Meta.fields:

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                'id',
                'first_name',
                'last_name',
                'email',
                'password'
            )

    Поле fields в классе Meta, в сериализаторе, отвечает за то, значения каких полей будет отправлено клиенту и за то,
    какие поля пользователю сделуюет заполнить, перед отправкой на сервер.
    Если у строкового поля модели указан параметр blank=True, то пользователь может отправить пустую строку.
    Если blank=False, то пользователь должен что то написать.

    Если в fields не указано какое то строковое поле, то это значит, что пользователю не нужно его заполнять, даже если
    у этого поля указан blank=False. В базу данных просто сохранится пустая строка.
    Ислкючением является поле, которое указано обязательным в менеджере модели. Например в менеджере модели User,
    обязательным полем является username. Соответственно менеджер, при сохранении объекта модели, просто не даст оставить
    это поле пустым.



    Generic Views:

    В пакете generics, джанго рест фреймворка, есть готовые вьюхи(Generic Views):

    1 CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

    2 ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView

    Внутри этих Generic Views реализованы методы вызываемые в ответ на get, post, put, patch и delete запросы.
    Их названия аналогичны этим запросам.

    1)
    В CreateAPIView реализован метод post - создает 1 объект в бд, в ответ на post запрос.
    В ListAPIView метод get - возвращающает список объектов
    В RetrieveAPIView метод get - возвращающает 1 объект
    В DestroyAPIView метод delete - удаляет 1 объект
    В UpdateAPIView реализованы put и patch методы. Первый отвечает за полное изменение объекта, второй за частичное.

    2)
    ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView - это Generic Views,
    совмещающие в себе разные комбинации простых Generic Views, описаных выше. Например ListCreateAPIView совмещает
    в себе ListAPIView и CreateAPIView и содержит в себе реализацию get и post методов.



    ModelMixins:

    Generic Views внутри своих get, post, put, patch и delete методов вызывают методы, которые отвечают за сериализацию
    данных, их сохранение или обновление, а также за возвращение Response ответа с данными.

    Эти методы они берут из классов, от которых наследуются. Эти классы называются ModelMixins. Они являются миксинами.

    Названия этих методов:
    create, list, retrieve, update, partial_update, destroy.
    Методы create и update миксинов не стоит путать с методами create и update сериализаторов.

    Методы create и update миксинов отвечают за то, чтобы:

    1 Взять конкретный сериализатор и передать ему данные для валидации
    serializer = self.get_serializer(data=request.data)
    
    2 Получить объект модели и передать в сериализатор вместе с данными, если это происходит внутри метода миксина update.
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)

    3 Вызвать метод is_valid с параметром raise_exception=True
    serializer.is_valid(raise_exception=True)

    4 Вызвать метод save сериализатора, внутри которого уже реализованы те самые методы create и update, которые отвечают
    за непосредственное изменение записей в самой базе данных.
    serializer.save()

    5 Возвратить ответ - объект Response
    
    Это примерное описание. Методы миксинов отличаются разными нюансами, в зависимости от своего назначения.

    В общем методы миксинов отвечают за вызов сериализатора и использование его методов, для сериализации, сохранения,
    обновления и возвращения данных через Response
    А методы create и update сериализатора отвечают, за непосредственное внесение изменений в базу данных.



    GenericAPIView:

    Generic Views от ModelMixins и от GenericAPIView
    class CreateAPIView(mixins.CreateModelMixin, GenericAPIView):

    От миксинов Generic Views берут методы create, list, retrieve, update, partial_update и destroy, отвечающие за
    использование сериализатора для сериализации, сохранения, обновления и возвращения данных.

    От GenericAPIView Generic Views берут переменные отвечающие за хранение списка(queryset) и сериализатора
    queryset и serializer_class
    А также берут методы:
    Получения списка queryset - get_queryset()
    Получения объекта модели - get_object(). Получает он его из queryset, используя аргументы фильтрации
    obj = get_object_or_404(queryset, **filter_kwargs)

    Получения сериализатора - get_serializer()
    Получения класса сериализатора - get_serializer_class()
    Получения контекста сериализатора - get_serializer_context()
    Фильтрацию списка queryset - filter_queryset()
    Методы отвечающие за пагинацию - paginator(), paginate_queryset(), get_paginated_response().
    А также метод as_view()

    Миксины же в свою очередь внутри своих методов create, list, retrieve, update, partial_update и destroy, используют
    методы GenericAPIView, перечисленные выше. То есть без GenericAPIView миксины не работают, они не самостоятельны.

    Для того, чтобы Generic Views работали, они наследуются из миксинов и GenericAPIView.
    То есть из миксина и GenericAPIView собирается полноценная вьюха Generic Views.

    Generic Views содержать методы get, post, put, patch, delete.
    Эти методы внутри себя вызывают методы ModelMixins - create, list, retrieve, update, partial_update и destroy
    Методы же миксинов внутри себя вызывают методы GenericAPIView - get_queryset, get_object, get_serializer и другие

    Методы миксинов называют экшенами(actions)
"""
