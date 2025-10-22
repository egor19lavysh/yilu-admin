from django.db import models
from django.core.exceptions import ValidationError

def validate_uppercase_letter(value):
    """Валидатор для проверки, что буква в верхнем регистре"""
    if not value.isupper() or len(value) != 1:
        raise ValidationError('Буква должна быть в верхнем регистре (A-Z)')

class ListeningHSK4(models.Model):
    """Основная модель варианта аудирования HSK4"""
    audio_id = models.CharField(max_length=255)
    
    class Meta:
        db_table = "hsk4_listening_tasks"


class FirstTaskHSK4(models.Model):
    """Задание первого типа HSK4 - текстовые вопросы с boolean ответом"""
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    listening_var = models.ForeignKey(
        ListeningHSK4,
        on_delete=models.CASCADE,
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk4_listening_first_tasks"


class SecondTaskHSK4(models.Model):
    """Задание второго типа HSK4 - вопросы с выбором буквы и вариантами"""
    correct_letter = models.CharField(
        max_length=1,
        validators=[validate_uppercase_letter]  # Добавлена валидация
    )
    listening_var = models.ForeignKey(
        ListeningHSK4,
        on_delete=models.CASCADE,
        related_name="second_type_tasks"
    )
    
    class Meta:
        db_table = "hsk4_listening_second_tasks"
    
    def clean(self):
        """Дополнительная валидация на уровне модели"""
        if self.correct_letter:
            self.correct_letter = self.correct_letter.upper()


class SecondTaskHSK4Option(models.Model):
    """Вариант ответа для задания второго типа HSK4"""
    letter = models.CharField(
        max_length=1,
        validators=[validate_uppercase_letter]  # Добавлена валидация
    )
    text = models.TextField()
    task = models.ForeignKey(
        SecondTaskHSK4,
        on_delete=models.CASCADE,
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk4_listening_second_task_options"
    
    def clean(self):
        """Дополнительная валидация на уровне модели"""
        if self.letter:
            self.letter = self.letter.upper()


class ThirdTaskHSK4(models.Model):
    """Задание третьего типа HSK4 - вопросы с выбором буквы и вариантами"""
    correct_letter = models.CharField(
        max_length=1,
        validators=[validate_uppercase_letter]  # Добавлена валидация
    )
    listening_var = models.ForeignKey(
        ListeningHSK4,
        on_delete=models.CASCADE,
        related_name="third_type_tasks"
    )
    
    class Meta:
        db_table = "hsk4_listening_third_tasks"
    
    def clean(self):
        """Дополнительная валидация на уровне модели"""
        if self.correct_letter:
            self.correct_letter = self.correct_letter.upper()


class ThirdTaskHSK4Option(models.Model):
    """Вариант ответа для задания третьего типа HSK4"""
    letter = models.CharField(
        max_length=1,
        validators=[validate_uppercase_letter]  # Добавлена валидация
    )
    text = models.TextField()
    task = models.ForeignKey(
        ThirdTaskHSK4,
        on_delete=models.CASCADE,
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk4_listening_third_task_options"
    
    def clean(self):
        """Дополнительная валидация на уровне модели"""
        if self.letter:
            self.letter = self.letter.upper()