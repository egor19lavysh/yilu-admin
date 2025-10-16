from django.db import models

class Writing(models.Model):
    class Meta:
        db_table = "writing_tasks"


class WritingFirstTask(models.Model):
    class Meta:
        db_table = "writing_first_tasks"
    
    chars = models.TextField()
    correct_answer = models.TextField()
    writing_var = models.ForeignKey(
        Writing,
        on_delete=models.CASCADE,
        related_name="first_tasks"
    )


class WritingSecondTask(models.Model):
    class Meta:
        db_table = "writing_second_tasks"
    
    text = models.TextField()
    correct_answer = models.TextField()
    writing_var = models.ForeignKey(
        Writing,
        on_delete=models.CASCADE,
        related_name="second_tasks"
    )