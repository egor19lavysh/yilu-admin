from django.db import models

class WritingHSK5(models.Model):
    """Основная модель варианта письма HSK5"""
    
    class Meta:
        db_table = "hsk5_writing_tasks"


class WritingFirstTaskHSK5(models.Model):
    """Задание первого типа письма HSK5 - составление предложения из слов"""
    correct_sentence = models.TextField()
    words = models.TextField()
    writing_var = models.ForeignKey(
        WritingHSK5,
        on_delete=models.CASCADE,
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk5_writing_first_tasks"


class WritingSecondTaskHSK5(models.Model):
    """Задание второго типа письма HSK5 - написание по тексту"""
    text = models.TextField()
    writing_var = models.ForeignKey(
        WritingHSK5,
        on_delete=models.CASCADE,
        related_name="second_type_tasks"
    )
    
    class Meta:
        db_table = "hsk5_writing_second_tasks"


class WritingThirdTaskHSK5(models.Model):
    """Задание третьего типа письма HSK5 - описание картинки"""
    picture_id = models.CharField(max_length=255)
    writing_var = models.ForeignKey(
        WritingHSK5,
        on_delete=models.CASCADE,
        related_name="third_type_tasks"
    )
    
    class Meta:
        db_table = "hsk5_writing_third_tasks"