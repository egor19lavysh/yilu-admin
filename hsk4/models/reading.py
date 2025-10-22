from django.db import models

class ReadingHSK4(models.Model):
    """Основная модель варианта чтения HSK4"""
    
    class Meta:
        db_table = "hsk4_reading_tasks"


class ReadingFirstTaskHSK4(models.Model):
    """Задание первого типа HSK4 - опции и предложения"""
    reading_var = models.ForeignKey(
        ReadingHSK4,
        on_delete=models.CASCADE,
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk4_reading_first_tasks"


class ReadingFirstTaskOptionHSK4(models.Model):
    """Опция для задания первого типа HSK4"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingFirstTaskHSK4,
        on_delete=models.CASCADE,
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk4_reading_first_task_options"


class ReadingFirstTaskSentenceHSK4(models.Model):
    """Предложение для задания первого типа HSK4"""
    correct_letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingFirstTaskHSK4,
        on_delete=models.CASCADE,
        related_name="sentences"
    )
    
    class Meta:
        db_table = "hsk4_reading_first_task_sentences"


class ReadingSecondTaskHSK4(models.Model):
    """Задание второго типа HSK4 - последовательность и опции"""
    correct_sequence = models.CharField(max_length=5)
    reading_var = models.ForeignKey(
        ReadingHSK4,
        on_delete=models.CASCADE,
        related_name="second_type_tasks"
    )
    
    class Meta:
        db_table = "hsk4_reading_second_tasks"


class ReadingSecondTaskOptionHSK4(models.Model):
    """Опция для задания второго типа HSK4"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingSecondTaskHSK4,
        on_delete=models.CASCADE,
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk4_reading_second_task_options"


class ReadingThirdTaskHSK4(models.Model):
    """Задание третьего типа HSK4 - текст с вопросами"""
    text = models.TextField()
    reading_var = models.ForeignKey(
        ReadingHSK4,
        on_delete=models.CASCADE,
        related_name="third_type_tasks"
    )
    
    class Meta:
        db_table = "hsk4_reading_third_tasks"


class ReadingThirdTaskQuestionHSK4(models.Model):
    """Вопрос для задания третьего типа HSK4"""
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingThirdTaskHSK4,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk4_reading_third_task_questions"


class QuestionOptionHSK4(models.Model):
    """Опция ответа для вопроса третьего типа HSK4"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    question = models.ForeignKey(
        ReadingThirdTaskQuestionHSK4,
        on_delete=models.CASCADE,
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk4_reading_third_task_question_options"