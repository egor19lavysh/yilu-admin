from django.db import models

class ListeningHSK5(models.Model):
    """Основная модель варианта аудирования HSK5"""
    audio_id = models.CharField(max_length=255)
    
    class Meta:
        db_table = "hsk5_listening_tasks"


class FirstTaskHSK5(models.Model):
    """Задание первого типа HSK5 - выбор из вариантов"""
    correct_letter = models.CharField(max_length=1)
    listening_var = models.ForeignKey(
        ListeningHSK5,
        on_delete=models.CASCADE,
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk5_listening_first_tasks"


class FirstTaskHSK5Option(models.Model):
    """Вариант ответа для задания первого типа HSK5"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        FirstTaskHSK5,
        on_delete=models.CASCADE,
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk5_listening_first_tasks_option"