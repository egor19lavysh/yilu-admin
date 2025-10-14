from django.db import models

class ListeningHSK1(models.Model):
    """Основная модель варианта аудирования HSK1"""
    audio_id = models.CharField(max_length=255)
    
    class Meta:
        db_table = "hsk1_listening_tasks"


class FirstTaskHSK1(models.Model):
    """Задание первого типа HSK1"""
    picture_id = models.CharField(max_length=255)
    listening_var = models.ForeignKey(
        ListeningHSK1, 
        on_delete=models.CASCADE, 
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk1_listening_first_tasks"


class FirstTaskHSK1Question(models.Model):
    """Вопрос для задания первого типа HSK1"""
    is_correct = models.BooleanField()
    task = models.ForeignKey(
        FirstTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk1_listening_first_tasks_questions"


class SecondTaskHSK1(models.Model):
    """Задание второго типа HSK1"""
    picture_id = models.CharField(max_length=255)
    listening_var = models.ForeignKey(
        ListeningHSK1, 
        on_delete=models.CASCADE, 
        related_name="second_type_tasks"
    )
    
    class Meta:
        db_table = "hsk1_listening_second_tasks"


class SecondTaskHSK1Question(models.Model):
    """Вопрос для задания второго типа HSK1"""
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        SecondTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk1_listening_second_tasks_questions"


class ThirdTaskHSK1(models.Model):
    """Задание третьего типа HSK1"""
    picture_id = models.CharField(max_length=255)
    listening_var = models.ForeignKey(
        ListeningHSK1, 
        on_delete=models.CASCADE, 
        related_name="third_type_tasks"
    )
    
    class Meta:
        db_table = "hsk1_listening_third_tasks"


class ThirdTaskHSK1Question(models.Model):
    """Вопрос для задания третьего типа HSK1"""
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ThirdTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk1_listening_third_tasks_questions"


class FourthTaskHSK1(models.Model):
    """Задание четвертого типа HSK1"""
    listening_var = models.ForeignKey(
        ListeningHSK1, 
        on_delete=models.CASCADE, 
        related_name="fourth_type_tasks"
    )
    
    class Meta:
        db_table = "hsk1_listening_fourth_tasks"


class FourthTaskHSK1Question(models.Model):
    """Вопрос для задания четвертого типа HSK1"""
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        FourthTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk1_listening_fourth_tasks_questions"


class FourthTaskHSK1Option(models.Model):
    """Вариант ответа для вопроса четвертого типа HSK1"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    question = models.ForeignKey(
        FourthTaskHSK1Question, 
        on_delete=models.CASCADE, 
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk1_listening_fourth_tasks_options"