from django.db import models

class WritingHSK4(models.Model):
    """Основная модель варианта письма HSK4"""
    
    class Meta:
        db_table = "hsk4_writing_tasks"


class WritingFirstTaskHSK4(models.Model):
    """Задание первого типа HSK4 - составление предложения из слов"""
    correct_sentence = models.TextField()
    words = models.TextField()
    writing_var = models.ForeignKey(
        WritingHSK4,
        on_delete=models.CASCADE,
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk4_writing_first_tasks"


class WritingSecondTaskHSK4(models.Model):
    """Задание второго типа HSK4 - описание картинки с использованием слов"""
    picture_id = models.CharField(max_length=255)
    writing_var = models.ForeignKey(
        WritingHSK4,
        on_delete=models.CASCADE,
        related_name="second_type_tasks"
    )
    
    class Meta:
        db_table = "hsk4_writing_second_tasks"


class WritingSecondTaskWord(models.Model):
    """Слово для задания второго типа HSK4"""
    text = models.TextField()
    possible_answer = models.TextField()
    task = models.ForeignKey(
        WritingSecondTaskHSK4,
        on_delete=models.CASCADE,
        related_name="words"
    )
    
    class Meta:
        db_table = "hsk4_writing_second_task_words"