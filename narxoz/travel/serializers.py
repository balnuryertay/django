import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Travel

# class TravelModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content

class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel
        fields = "__all__"

# def encode():
#     model = TravelModel('Вашингтон', 'США астанасы')
#     model_sr = TravelSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Вашингтон","content":"США астанасы"}')
#     data = JSONParser().parse(stream)
#     serializer = TravelSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)