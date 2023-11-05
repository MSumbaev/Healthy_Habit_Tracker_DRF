from rest_framework.exceptions import ValidationError


class RewardOrLinkedValidator:
    """Валидатор на одновременное заполнение полей 'linked' и 'reward'"""
    def __init__(self, reward, linked):
        self.reward = reward
        self.linked = linked

    def __call__(self, value):
        habits_reward = dict(value).get(self.reward)
        habits_linked = dict(value).get(self.linked)

        if habits_reward and habits_linked:
            raise ValidationError('Нельзя выбрать одновременно связанную привычку и вознаграждение!')
        elif habits_reward is None and habits_linked is None:
            return


class ExecutionDurationValidator:
    """Валидатор на продолжительность действия 'length'"""
    def __init__(self, length):
        self.length = length

    def __call__(self, value):
        habits_length = dict(value).get(self.length)

        if habits_length is None:
            return
        elif int(habits_length) > 120:
            raise ValidationError('Время выполнения должно быть не больше 120 секунд!')


class LinkedHabitsValidator:
    """Валидатор на то, что в связанные привычки могут попадать только привычки с признаком приятной привычки"""
    def __init__(self, linked):
        self.linked = linked

    def __call__(self, value):
        linked_habit = value.get(self.linked)

        if linked_habit is not None:
            if not linked_habit.is_pleasant:
                raise ValidationError(
                    'В связанные привычки могут попадать только привычки с признаком приятной привычки!'
                )
        else:
            return


class PleasantHabitValidator:
    """Валидатор на то, что у приятной привычки не может быть вознаграждения или связанной привычки"""
    def __init__(self, reward, linked, is_pleasant):
        self.reward = reward
        self.linked = linked
        self.is_pleasant = is_pleasant

    def __call__(self, value):
        pleasant_habit = dict(value).get(self.is_pleasant)
        habits_reward = dict(value).get(self.reward)
        habits_linked = dict(value).get(self.linked)

        if pleasant_habit is None and habits_linked is None and habits_linked is None:
            return

        if pleasant_habit:
            if habits_reward or habits_linked:
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки!')


class PeriodValidator:
    """Валидатор на правильное задание поля 'period'"""
    def __init__(self, period):
        self.period = period

    def __call__(self, value):
        habits_period = dict(value).get(self.period)

        if habits_period is None:
            return
        elif int(habits_period) > 7:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней!')
        elif int(habits_period) < 1:
            raise ValidationError('Периодичность не может быть меньше 1!')
