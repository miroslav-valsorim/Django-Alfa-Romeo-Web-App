from rest_framework import serializers

from alfa_romeo_web.news.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
