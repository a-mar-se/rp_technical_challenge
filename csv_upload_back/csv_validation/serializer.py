from django.forms import FloatField
from rest_framework.serializers import ModelSerializer,  CharField
from .models import  Entity

class EntitySerializer (ModelSerializer):     
    entity_id = CharField(max_length=8)
    data_type = CharField(max_length=16)
    sender_video = CharField(max_length=256)

    class Meta: 
        # print('Meta in XalenxSerializer')   
        model = Entity
        fields = '__all__'

