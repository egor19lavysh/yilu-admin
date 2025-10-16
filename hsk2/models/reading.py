from django.db import models


class ReadingHSK2(models.Model):
    class Meta:
        db_table = "hsk2_reading_tasks"


class ReadingFirstTaskHSK2(models.Model):
    picture_id = models.CharField(max_length=255)
    reading_var = models.ForeignKey(
        ReadingHSK2, 
        on_delete=models.CASCADE, 
        related_name="first_type_tasks"
    )
    
    class Meta:
        db_table = "hsk2_reading_first_tasks"


class ReadingFirstTaskHSK2Sentence(models.Model):
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingFirstTaskHSK2, 
        on_delete=models.CASCADE, 
        related_name="sentences"
    )
    
    class Meta:
        db_table = "hsk2_reading_first_tasks_sentences"


class ReadingSecondTaskHSK2(models.Model):
    reading_var = models.ForeignKey(
        ReadingHSK2, 
        on_delete=models.CASCADE, 
        related_name="second_type_tasks"
    )
    
    class Meta:
        db_table = "hsk2_reading_second_tasks"


class ReadingSecondTaskHSK2Option(models.Model):
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingSecondTaskHSK2, 
        on_delete=models.CASCADE, 
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk2_reading_second_tasks_options"


class ReadingSecondTaskHSK2Sentence(models.Model):
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingSecondTaskHSK2, 
        on_delete=models.CASCADE, 
        related_name="sentences"
    )
    
    class Meta:
        db_table = "hsk2_reading_second_tasks_sentences"


class ReadingThirdTaskHSK2(models.Model):
    first_sentence = models.TextField()
    second_sentence = models.TextField()
    is_correct = models.BooleanField()
    reading_var = models.ForeignKey(
        ReadingHSK2, 
        on_delete=models.CASCADE, 
        related_name="third_type_tasks"
    )
    
    class Meta:
        db_table = "hsk2_reading_third_tasks"


class ReadingFourthTaskHSK2(models.Model):
    reading_var = models.ForeignKey(
        ReadingHSK2, 
        on_delete=models.CASCADE, 
        related_name="fourth_type_tasks"
    )
    
    class Meta:
        db_table = "hsk2_reading_fourth_tasks"


class ReadingFourthTaskHSK2Option(models.Model):
    letter = models.CharField(max_length=1)
    text = models.TextField()
    task = models.ForeignKey(
        ReadingFourthTaskHSK2, 
        on_delete=models.CASCADE, 
        related_name="options"
    )
    
    class Meta:
        db_table = "hsk2_reading_fourth_tasks_options"


class ReadingFourthTaskHSK2Question(models.Model):
    text = models.TextField()
    correct_letter = models.CharField(max_length=1)
    task = models.ForeignKey(
        ReadingFourthTaskHSK2, 
        on_delete=models.CASCADE, 
        related_name="questions"
    )
    
    class Meta:
        db_table = "hsk2_reading_fourth_tasks_questions"