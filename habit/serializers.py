from rest_framework import serializers

from habit.models import Habit
from habit.validators import RewardOrLinkedValidator, ExecutionDurationValidator, LinkedHabitsValidator, \
    PleasantHabitValidator, PeriodValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RewardOrLinkedValidator(),
            ExecutionDurationValidator(),
            LinkedHabitsValidator(),
            PleasantHabitValidator(),
            PeriodValidator()
        ]
