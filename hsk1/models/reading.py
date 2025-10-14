from django.db import models

class ReadingHSK1(models.Model):
    """Основная модель варианта чтения HSK1"""
    
    class Meta:
        db_table = "hsk1_reading_tasks"


class ReadingFirstTaskHSK1(models.Model):
    """Задание первого типа чтения HSK1"""
    picture_id = models.CharField(max_length=255)
    reading_var = models.ForeignKey(
        ReadingHSK1, 
        on_delete=models.CASCADE, 
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk1_reading_first_tasks"


class ReadingFirstTaskHSK1Option(models.Model):
    """Вариант для задания первого типа чтения HSK1"""
    is_correct = models.BooleanField()
    task = models.ForeignKey(
        ReadingFirstTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk1_reading_first_tasks_options"


class ReadingSecondTaskHSK1(models.Model):
    """Задание второго типа чтения HSK1"""
    picture_id = models.CharField(max_length=255)
    reading_var = models.ForeignKey(
        ReadingHSK1, 
        on_delete=models.CASCADE, 
        related_name="second_type_tasks"
    )
    
    class Meta:
        db_table = "hsk1_reading_second_tasks"


class ReadingSecondTaskHSK1Sentence(models.Model):
    """Предложение для задания второго типа чтения HSK1"""
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingSecondTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="sentences"
    )
    
    class Meta:
        db_table = "hsk1_reading_second_tasks_sentences"


class ReadingThirdTaskHSK1(models.Model):
    """Задание третьего типа чтения HSK1"""
    reading_var = models.ForeignKey(
        ReadingHSK1, 
        on_delete=models.CASCADE, 
        related_name="third_type_tasks"
    )
    
    class Meta:
        db_table = "hsk1_reading_third_tasks"


class ReadingThirdTaskHSK1Sentence(models.Model):
    """Предложение для задания третьего типа чтения HSK1"""
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingThirdTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="sentences"
    )
    
    class Meta:
        db_table = "hsk1_reading_third_tasks_sentences"


class ReadingThirdTaskHSK1Option(models.Model):
    """Вариант для задания третьего типа чтения HSK1"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingThirdTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk1_reading_third_tasks_options"


class ReadingFourthTaskHSK1(models.Model):
    """Задание четвертого типа чтения HSK1"""
    reading_var = models.ForeignKey(
        ReadingHSK1, 
        on_delete=models.CASCADE, 
        related_name="fourth_type_tasks"
    )
    
    class Meta:
        db_table = "hsk1_reading_fourth_tasks"


class ReadingFourthTaskHSK1Option(models.Model):
    """Вариант для задания четвертого типа чтения HSK1"""
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingFourthTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk1_reading_fourth_tasks_options"


class ReadingFourthTaskHSK1Sentence(models.Model):
    """Предложение для задания четвертого типа чтения HSK1"""
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingFourthTaskHSK1, 
        on_delete=models.CASCADE, 
        related_name="sentences"
    )
    
    class Meta:
        db_table = "hsk1_reading_fourth_tasks_sentences"