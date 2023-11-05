from rest_framework import serializers

from habit.models import Habit
from habit.validators import RewardOrLinkedValidator, ExecutionDurationValidator, LinkedHabitsValidator, \
    PleasantHabitValidator, PeriodValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            RewardOrLinkedValidator(reward='reward', linked='linked',),
            ExecutionDurationValidator(length='length',),
            LinkedHabitsValidator(linked='linked',),
            PleasantHabitValidator(reward='reward', linked='linked', is_pleasant='is_pleasant',),
            PeriodValidator(period='period')
        ]
