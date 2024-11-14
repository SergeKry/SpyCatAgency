from rest_framework import serializers
from .models import SpyCat, Mission, Target
from .breeds import get_breeds
from django.db import transaction


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


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['name', 'country', 'notes', 'complete']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['cat', 'complete', 'targets']

    def validate_targets(self, value):
        if not (1 <= len(value) <= 3):
            raise serializers.ValidationError("A mission assumes a range of targets (minimum: 1, maximum: 3)")
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')

        # Saving mission
        mission = Mission(**validated_data)
        mission.save()

        # Saving targets
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['complete', 'notes']

    def validate(self, data):
        """Here we check if mission is completed, so we do not allow to update notes"""
        target = self.instance
        if target.mission.complete or target.complete:
            if 'notes' in data:
                raise serializers.ValidationError("Notes cannot be updated if the target or the mission is completed.")
        return data
