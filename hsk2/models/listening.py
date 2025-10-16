from django.db import models

class ListeningHSK2(models.Model):
    """Основная модель варианта аудирования HSK2"""
    audio_id = models.CharField(max_length=255)
    
    class Meta:
        db_table = "hsk2_listening_tasks"


class FirstTaskHSK2(models.Model):
    """Задание первого типа HSK2"""
    picture_id = models.CharField(max_length=255)
    listening_var = models.ForeignKey(
        ListeningHSK2, 
        on_delete=models.CASCADE, 
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk2_listening_first_tasks"


class FirstTaskHSK2Question(models.Model):
    """Вопрос для задания первого типа HSK2"""
    is_correct = models.BooleanField()
    task = models.ForeignKey(
        FirstTaskHSK2, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk2_listening_first_tasks_questions"


class SecondTaskHSK2(models.Model):
    """Задание второго типа HSK2"""
    picture_id = models.CharField(max_length=255)
    listening_var = models.ForeignKey(
        ListeningHSK2, 
        on_delete=models.CASCADE, 
        related_name="second_type_tasks"
    )
    
    class Meta:
        db_table = "hsk2_listening_second_tasks"


class SecondTaskHSK2Question(models.Model):
    """Вопрос для задания второго типа HSK2"""
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        SecondTaskHSK2, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk2_listening_second_tasks_questions"


class ThirdTaskHSK2(models.Model):
    """Задание третьего типа HSK2"""
    listening_var = models.ForeignKey(
        ListeningHSK2, 
        on_delete=models.CASCADE, 
        related_name="third_type_tasks"
    )
    
    class Meta:
        db_table = "hsk2_listening_third_tasks"


class ThirdTaskHSK2Question(models.Model):
    """Вопрос для задания третьего типа HSK2"""
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ThirdTaskHSK2, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk2_listening_third_tasks_questions"


class ThirdTaskHSK2Option(models.Model):
    """Вариант ответа для вопроса третьего типа HSK2"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    question = models.ForeignKey(
        ThirdTaskHSK2Question, 
        on_delete=models.CASCADE, 
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk2_listening_third_tasks_options"