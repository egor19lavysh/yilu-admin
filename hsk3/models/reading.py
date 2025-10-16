from django.db import models

class Reading(models.Model):
    class Meta:
        db_table = "reading_tasks"


class ReadingFirstTask(models.Model):
    class Meta:
        db_table = "reading_first_tasks"
    
    reading_var = models.ForeignKey(
        Reading,
        on_delete=models.CASCADE,
        related_name="first_tasks"
    )


class ReadingFirstTaskOption(models.Model):
    class Meta:
        db_table = "reading_first_task_options"
    
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingFirstTask,
        on_delete=models.CASCADE,
        related_name="options"
    )


class ReadingFirstTaskQuestion(models.Model):
    class Meta:
        db_table = "reading_first_task_questions"
    
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingFirstTask,
        on_delete=models.CASCADE,
        related_name="questions"
    )


class ReadingSecondTask(models.Model):
    class Meta:
        db_table = "reading_second_tasks"
    
    reading_var = models.ForeignKey(
        Reading,
        on_delete=models.CASCADE,
        related_name="second_tasks"
    )


class ReadingSecondTaskOption(models.Model):
    class Meta:
        db_table = "reading_second_task_options"
    
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingSecondTask,
        on_delete=models.CASCADE,
        related_name="options"
    )


class ReadingSecondTaskQuestion(models.Model):
    class Meta:
        db_table = "reading_second_task_questions"
    
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingSecondTask,
        on_delete=models.CASCADE,
        related_name="questions"
    )


class ReadingThirdTask(models.Model):
    class Meta:
        db_table = "reading_third_tasks"
    
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    reading_var = models.ForeignKey(
        Reading,
        on_delete=models.CASCADE,
        related_name="third_tasks"
    )


class ReadingThirdTaskOption(models.Model):
    class Meta:
        db_table = "reading_third_task_options"
    
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingThirdTask,
        on_delete=models.CASCADE,
        related_name="options"
    )