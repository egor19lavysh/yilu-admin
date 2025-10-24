from django.db import models

class ReadingHSK5(models.Model):
    """Основная модель варианта чтения HSK5"""
    
    class Meta:
        db_table = "hsk5_reading_tasks"


class ReadingFirstTaskHSK5(models.Model):
    """Задание первого типа чтения HSK5 - текст с вопросами"""
    text = models.TextField()
    reading_var = models.ForeignKey(
        ReadingHSK5,
        on_delete=models.CASCADE,
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk5_reading_first_tasks"


class ReadingFirstTaskHSK5Question(models.Model):
    """Вопрос для задания первого типа чтения HSK5"""
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingFirstTaskHSK5,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk5_reading_first_tasks_questions"


class ReadingFirstTaskQuestionOptionHSK5(models.Model):
    """Вариант ответа для вопроса первого типа чтения HSK5"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    question = models.ForeignKey(
        ReadingFirstTaskHSK5Question,
        on_delete=models.CASCADE,
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk5_reading_first_tasks_question_options"


class ReadingSecondTaskHSK5(models.Model):
    """Задание второго типа чтения HSK5 - выбор из вариантов"""
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    reading_var = models.ForeignKey(
        ReadingHSK5,
        on_delete=models.CASCADE,
        related_name="second_type_tasks"
    )
    
    class Meta:
        db_table = "hsk5_reading_second_tasks"


class ReadingSecondTaskHSK5Option(models.Model):
    """Вариант ответа для задания второго типа чтения HSK5"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingSecondTaskHSK5,
        on_delete=models.CASCADE,
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk5_reading_second_tasks_option"


class ReadingThirdTaskHSK5(models.Model):
    """Задание третьего типа чтения HSK5 - текст (возможно с фото) с вопросами"""
    photo_id = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    reading_var = models.ForeignKey(
        ReadingHSK5,
        on_delete=models.CASCADE,
        related_name="third_type_tasks"
    )
    
    class Meta:
        db_table = "hsk5_reading_third_tasks"


class ReadingThirdTaskHSK5Question(models.Model):
    """Вопрос для задания третьего типа чтения HSK5"""
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingThirdTaskHSK5,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk5_reading_third_tasks_questions"


class ReadingThirdTaskQuestionOptionHSK5(models.Model):
    """Вариант ответа для вопроса третьего типа чтения HSK5"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    question = models.ForeignKey(
        ReadingThirdTaskHSK5Question,
        on_delete=models.CASCADE,
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk5_reading_third_task_question_options"