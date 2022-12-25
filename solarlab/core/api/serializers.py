from rest_framework import serializers

class CountryInfoSerializer(serializers.Serializer):
    flag_link = serializers.URLField()
    capital = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    largest_city = serializers.CharField()
    official_languages = serializers.ListField(child=serializers.CharField())
    area_total = serializers.CharField()
    population = serializers.CharField()
    GDP_nominal = serializers.CharField()