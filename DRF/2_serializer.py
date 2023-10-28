from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    image = serializers.ImageField(read_only=True)
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        print(validated_data)
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.image = validated_data.get('image', instance.image)

        if validated_data['password']:
            instance.set_password(validated_data['password'])

        instance.save()

        return instance


class UserAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)

        return Response({'user': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = User.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = UserSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'user': serializer.data})


"""
    View отвечает за обработку запросов, а сериализатор за обработку и сохранение данных.
    А конкретно за их валидацию, конвертацию и сохранение.

    Если мы передаем данные клиенту из базы, то сериализатор конвертирует их из объектов модели в словарь или список
    упорядоченных словарей.
    При конвертации занчения не валидируются, так как достаются из базы данных.

    Если мы принимаем данные от клиента, то сериализатор валидирует их и создает словарь validated_data



    Если мы передаем в сериализатор список объектов(QuerySet), вместо одного, то при инициализации класса сериализатора,
    по мимо передачи QuerySet, также нужно указать параметр many=True. Сообщающий о том, что объект модели не один.
    serializer = UserSerializer(users, many=True)

    Если мы принимаем данные от клиента и хотим прогнать их через сериализатор с целью валидации, то данные нужно передать
    в именованный параметр data.
    serializer = UserSerializer(data=request.data).

    Перед сохранением стоит вызвать метод is_valid() с параметром raise_exception=True
    Если данные не прошли проверку, то этот метод вернет клиенту json строку с указанием на ошибок.
    serializer.is_valid(raise_exception=True)



    Метод сериализатора save() под капотом вызывает либо метод create() либо метод update(), в зависимости от
    переданных в класс сериализатор аргументов.
    Метод create() отвечает за создание новой записи в базе данных.
    Метод update() отвечает за изменение существующей записи.

    Если в сериализатор передан только параметр data, то при сохранении(serializer.save()) будет вызван метод
    create().
    serializer = UserSerializer(data=request.data)

    Если дополнительно передать параметр instance, при сохранении(serializer.save()) будет вызван метод update().
    serializer = UserSerializer(data=request.data, instance=instance)

    Методы сериализатора create() и update() нужно определить самому, так как их конкретной реализации нет в
    родительском классе. Там только их обозначение. Речь идет о родительском классе serializers.Serializer.
    В serializers.ModelSerializer эти методы уже определены.
"""