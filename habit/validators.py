from rest_framework.exceptions import ValidationError


class RewardOrLinkedValidator:
    def __call__(self, data):
        habits_reward = data.get('reward')
        habits_linked = data.get('linked')

        if habits_reward and habits_linked:
            raise ValidationError('Нельзя выбрать одновременно связанную привычку и вознаграждение!')


class ExecutionDurationValidator:
    def __call__(self, data):
        habits_length = data.get('length')

        if habits_length > 120:
            raise ValidationError('Время выполнения должно быть не больше 120 секунд!')


class LinkedHabitsValidator:
    def __call__(self, data):
        linked_habit = data.get('linked')

        if linked_habit is not None:
            if not linked_habit.is_pleasant:
                raise ValidationError(
                    'В связанные привычки могут попадать только привычки с признаком приятной привычки!'
                )


class PleasantHabitValidator:
    def __call__(self, data):
        pleasant_habit = data.get('is_pleasant')
        habits_reward = data.get('reward')
        habits_linked = data.get('linked')

        if pleasant_habit:
            if habits_reward or habits_linked:
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки!')


class PeriodValidator:
    def __call__(self, data):
        period = data.get('period')

        if period > 7:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней!')

        if period < 1:
            raise ValidationError('Периодичность не может быть меньше 1!')


