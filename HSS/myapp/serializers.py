# Serializers for mode and state REST services - serializers.py

from myapp.models import Mode
from rest_framework import serializers

class ModeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mode
        fields = ('url', 'name')

