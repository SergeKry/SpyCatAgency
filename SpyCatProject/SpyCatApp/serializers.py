from rest_framework import serializers
from .models import SpyCat
from .breeds import get_breeds


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'

    def validate_breed(self, value):
        allowed_breeds = get_breeds()
        if value not in allowed_breeds:
            raise serializers.ValidationError(f"{value} is not a valid breed.")
        return value


class EditSpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'
        read_only_fields = ['name', 'years_of_experience', 'breed']