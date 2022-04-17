from .models import *
from rest_framework.serializers import ModelSerializer
from drf_base64.fields import Base64ImageField, Base64FileField



class CustomerSerializer(ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = Customer
        fields = '__all__'        