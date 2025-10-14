from django import forms
from .models import *
from django.forms import inlineformset_factory

# Основная форма для варианта аудирования
class ListeningVariantForm(forms.ModelForm):
    class Meta:
        model = ListeningHSK1
        fields = ['audio_id']
        labels = {'audio_id': 'ID аудио файла'}


# Форма для задания 1 типа (с вопросами)
class Task1Form(forms.ModelForm):
    class Meta:
        model = FirstTaskHSK1
        fields = ['picture_id']
        labels = {'picture_id': 'ID картинки для задания 1'}


# Форма для вопроса задания 1 типа
class Task1QuestionForm(forms.ModelForm):
    class Meta:
        model = FirstTaskHSK1Question
        fields = ['is_correct']
        labels = {'is_correct': 'Это правильный ответ?'}


# Форма для задания 2 типа (с вопросами)
class Task2Form(forms.ModelForm):
    class Meta:
        model = SecondTaskHSK1
        fields = ['picture_id']
        labels = {'picture_id': 'ID картинки для задания 2'}


# Форма для вопроса задания 2 типа
class Task2QuestionForm(forms.ModelForm):
    class Meta:
        model = SecondTaskHSK1Question
        fields = ['correct_letter']
        labels = {'correct_letter': 'Правильная буква (A/B/C)'}


# Форма для задания 3 типа (с вопросами)
class Task3Form(forms.ModelForm):
    class Meta:
        model = ThirdTaskHSK1
        fields = ['picture_id']
        labels = {'picture_id': 'ID картинки для задания 3'}


# Форма для вопроса задания 3 типа
class Task3QuestionForm(forms.ModelForm):
    class Meta:
        model = ThirdTaskHSK1Question
        fields = ['correct_letter']
        labels = {'correct_letter': 'Правильная буква (A/B/C)'}


# Форма для задания 4 типа
class Task4Form(forms.ModelForm):
    class Meta:
        model = FourthTaskHSK1
        fields = []  # Нет своих полей, только связь


# Форма для вопроса задания 4 типа
class Task4QuestionForm(forms.ModelForm):
    class Meta:
        model = FourthTaskHSK1Question
        fields = ['correct_letter']
        labels = {'correct_letter': 'Правильная буква (A/B/C)'}


# Форма для варианта ответа задания 4 типа
class Task4OptionForm(forms.ModelForm):
    class Meta:
        model = FourthTaskHSK1Option
        fields = ['letter', 'text']
        labels = {
            'letter': 'Буква варианта (A/B/C/D)',
            'text': 'Текст варианта'
        }


Task1QuestionFormSet = inlineformset_factory(
    FirstTaskHSK1,
    FirstTaskHSK1Question,
    form=Task1QuestionForm,
    extra=5,  # 5 вопросов в первом задании
    can_delete=False
)

# FormSet для вопросов задания 2 (обычно 5 вопросов)
Task2QuestionFormSet = inlineformset_factory(
    SecondTaskHSK1,
    SecondTaskHSK1Question,
    form=Task2QuestionForm,
    extra=5,
    can_delete=False
)

# FormSet для вопросов задания 3 (обычно 5 вопросов)
Task3QuestionFormSet = inlineformset_factory(
    ThirdTaskHSK1,
    ThirdTaskHSK1Question,
    form=Task3QuestionForm,
    extra=5,
    can_delete=False
)

# FormSet для вопросов задания 4 (обычно 10 вопросов)
Task4QuestionFormSet = inlineformset_factory(
    FourthTaskHSK1,
    FourthTaskHSK1Question,
    form=Task4QuestionForm,
    extra=10,
    can_delete=False
)

# FormSet для вариантов ответов к каждому вопросу задания 4
Task4OptionFormSet = inlineformset_factory(
    FourthTaskHSK1Question,
    FourthTaskHSK1Option,
    form=Task4OptionForm,
    extra=4,  # 4 варианта ответа на каждый вопрос
    can_delete=False
)