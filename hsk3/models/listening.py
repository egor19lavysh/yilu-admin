from django.db import models

class Listening(models.Model):
    class Meta:
        db_table = "listening_tasks"
    
    audio_id = models.CharField(max_length=255)

class FirstTask(models.Model):
    class Meta:
        db_table = "listening_first_tasks"
    
    picture_id = models.CharField(max_length=255)
    listening_var = models.ForeignKey(
        Listening, 
        on_delete=models.CASCADE,
        related_name="first_type_tasks"
    )

class FirstTaskQuestion(models.Model):
    class Meta:
        db_table = "listening_first_task_questions"
    
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        FirstTask, 
        on_delete=models.CASCADE,
        related_name="questions"
    )

class SecondTask(models.Model):
    class Meta:
        db_table = "listening_second_tasks"
    
    text = models.TextField()
    is_correct = models.BooleanField()
    listening_var = models.ForeignKey(
        Listening, 
        on_delete=models.CASCADE,
        related_name="second_type_tasks"
    )

class ThirdTask(models.Model):
    class Meta:
        db_table = "listening_third_tasks"
    
    listening_var = models.ForeignKey(
        Listening, 
        on_delete=models.CASCADE,
        related_name="third_type_tasks"
    )

class ThirdTaskQuestion(models.Model):
    class Meta:
        db_table = "listening_third_task_questions"
    
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ThirdTask, 
        on_delete=models.CASCADE,
        related_name="questions"
    )

class ThirdTaskOption(models.Model):
    class Meta:
        db_table = "listening_third_task_options"
    
    letter = models.CharField(max_length=1)
    text = models.TextField()
    question = models.ForeignKey(
        ThirdTaskQuestion, 
        on_delete=models.CASCADE,
        related_name="options"
    )