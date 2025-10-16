from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .models import *

def get_sections(request):
    return render(request, "hsk2/sections.html")


class ListeningListView(ListView):
    model = ListeningHSK2
    template_name = 'hsk2/listening_list.html'
    context_object_name = 'listening_variants'

class ListeningCreateView(CreateView):
    model = ListeningHSK2
    template_name = 'hsk2/listening_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант
            audio_id = request.POST.get('audio_id')
            listening_var = ListeningHSK2.objects.create(audio_id=audio_id)
            
            # 2. Задание 1 (10 boolean вопросов)
            task1_picture = request.POST.get('task1_picture_id')
            task1 = FirstTaskHSK2.objects.create(
                picture_id=task1_picture,
                listening_var=listening_var
            )
            for i in range(1, 11):
                is_correct = request.POST.get(f'task1_question_{i}') == 'true'
                FirstTaskHSK2Question.objects.create(
                    is_correct=is_correct,
                    task=task1
                )
            
            # 3. Задание 2 (5 вопросов A-F)
            task2_picture = request.POST.get('task2_picture_id')
            task2 = SecondTaskHSK2.objects.create(
                picture_id=task2_picture,
                listening_var=listening_var
            )
            for i in range(1, 6):
                correct_letter = request.POST.get(f'task2_question_{i}')
                SecondTaskHSK2Question.objects.create(
                    correct_letter=correct_letter,
                    task=task2
                )
            
            # 4. Задание 3 (5 вопросов A-F) - используем SecondTaskHSK2
            task3_picture = request.POST.get('task3_picture_id')
            task3 = SecondTaskHSK2.objects.create(
                picture_id=task3_picture,
                listening_var=listening_var
            )
            for i in range(1, 6):
                correct_letter = request.POST.get(f'task3_question_{i}')
                SecondTaskHSK2Question.objects.create(
                    correct_letter=correct_letter,
                    task=task3
                )
            
            # 5. Задание 4 (10 вопросов с вариантами A-C)
            task4 = ThirdTaskHSK2.objects.create(listening_var=listening_var)
            for i in range(1, 11):
                correct_letter = request.POST.get(f'task4_question_{i}')
                question = ThirdTaskHSK2Question.objects.create(
                    correct_letter=correct_letter,
                    task=task4
                )
                # Варианты ответов
                for letter in ['A', 'B', 'C']:
                    option_text = request.POST.get(f'task4_option{letter}_{i}')
                    ThirdTaskHSK2Option.objects.create(
                        letter=letter,
                        text=option_text,
                        question=question
                    )
            
            # 6. Задание 5 (5 вопросов с вариантами A-C) - используем ThirdTaskHSK2
            task5 = ThirdTaskHSK2.objects.create(listening_var=listening_var)
            for i in range(1, 6):
                correct_letter = request.POST.get(f'task5_question_{i}')
                question = ThirdTaskHSK2Question.objects.create(
                    correct_letter=correct_letter,
                    task=task5
                )
                # Варианты ответов
                for letter in ['A', 'B', 'C']:
                    option_text = request.POST.get(f'task5_option{letter}_{i}')
                    ThirdTaskHSK2Option.objects.create(
                        letter=letter,
                        text=option_text,
                        question=question
                    )
            
            return redirect('hsk2:listening_detail', pk=listening_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class ListeningDetailView(DetailView):
    model = ListeningHSK2
    template_name = 'hsk2/listening_detail.html'
    context_object_name = 'listening'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listening = self.object
        
        # Получаем все задания для отображения
        context['task1'] = listening.first_type_tasks.first()
        
        # Для заданий 2 и 3 используем SecondTaskHSK2
        second_tasks = list(listening.second_type_tasks.all())
        if len(second_tasks) > 0:
            context['task2'] = second_tasks[0]  # Первое задание второго типа
        if len(second_tasks) > 1:
            context['task3'] = second_tasks[1]  # Второе задание второго типа
        
        # Для заданий 4 и 5 используем ThirdTaskHSK2
        third_tasks = list(listening.third_type_tasks.all())
        if len(third_tasks) > 0:
            context['task4'] = third_tasks[0]  # Первое задание третьего типа
        if len(third_tasks) > 1:
            context['task5'] = third_tasks[1]  # Второе задание третьего типа
        
        return context

class ListeningUpdateView(UpdateView):
    model = ListeningHSK2
    template_name = 'hsk2/listening_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        listening = self.object
        context['listening'] = listening
        context['is_update'] = True
        
        # Задание 1
        task1 = listening.first_type_tasks.first()
        if task1:
            context['task1_picture_id'] = task1.picture_id
            context['task1_questions'] = list(task1.questions.all())
        
        # Задания 2 и 3 (SecondTaskHSK2)
        second_tasks = list(listening.second_type_tasks.all())
        if len(second_tasks) > 0:
            context['task2_picture_id'] = second_tasks[0].picture_id
            context['task2_questions'] = list(second_tasks[0].questions.all())
        if len(second_tasks) > 1:
            context['task3_picture_id'] = second_tasks[1].picture_id
            context['task3_questions'] = list(second_tasks[1].questions.all())
        
        # Задания 4 и 5 (ThirdTaskHSK2)
        third_tasks = list(listening.third_type_tasks.all())
        if len(third_tasks) > 0:
            task4_questions = list(third_tasks[0].questions.all())
            context['task4_questions'] = task4_questions
            # Собираем варианты ответов для задания 4
            task4_options = {}
            for question in task4_questions:
                task4_options[question.id] = {opt.letter: opt.text for opt in question.options.all()}
            context['task4_options'] = task4_options
        
        if len(third_tasks) > 1:
            task5_questions = list(third_tasks[1].questions.all())
            context['task5_questions'] = task5_questions
            # Собираем варианты ответов для задания 5
            task5_options = {}
            for question in task5_questions:
                task5_options[question.id] = {opt.letter: opt.text for opt in question.options.all()}
            context['task5_options'] = task5_options
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        listening = self.object
        
        try:
            # 1. Обновляем основной вариант
            audio_id = request.POST.get('audio_id')
            listening.audio_id = audio_id
            listening.save()
            
            # 2. Обновляем Задание 1
            task1 = listening.first_type_tasks.first()
            if task1:
                task1.picture_id = request.POST.get('task1_picture_id')
                task1.save()
                # Обновляем вопросы задания 1
                questions = list(task1.questions.all())
                for i in range(1, 11):
                    if i <= len(questions):
                        questions[i-1].is_correct = request.POST.get(f'task1_question_{i}') == 'true'
                        questions[i-1].save()
            
            # 3. Обновляем Задание 2
            second_tasks = list(listening.second_type_tasks.all())
            if len(second_tasks) > 0:
                task2 = second_tasks[0]
                task2.picture_id = request.POST.get('task2_picture_id')
                task2.save()
                # Обновляем вопросы задания 2
                questions = list(task2.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].correct_letter = request.POST.get(f'task2_question_{i}')
                        questions[i-1].save()
            
            # 4. Обновляем Задание 3
            if len(second_tasks) > 1:
                task3 = second_tasks[1]
                task3.picture_id = request.POST.get('task3_picture_id')
                task3.save()
                # Обновляем вопросы задания 3
                questions = list(task3.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].correct_letter = request.POST.get(f'task3_question_{i}')
                        questions[i-1].save()
            
            # 5. Обновляем Задание 4
            third_tasks = list(listening.third_type_tasks.all())
            if len(third_tasks) > 0:
                task4 = third_tasks[0]
                # Обновляем вопросы и варианты задания 4
                questions = list(task4.questions.all())
                for i in range(1, 11):
                    if i <= len(questions):
                        question = questions[i-1]
                        question.correct_letter = request.POST.get(f'task4_question_{i}')
                        question.save()
                        # Обновляем варианты ответов
                        for letter in ['A', 'B', 'C']:
                            option_text = request.POST.get(f'task4_option{letter}_{i}')
                            option = question.options.filter(letter=letter).first()
                            if option:
                                option.text = option_text
                                option.save()
            
            # 6. Обновляем Задание 5
            if len(third_tasks) > 1:
                task5 = third_tasks[1]
                # Обновляем вопросы и варианты задания 5
                questions = list(task5.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        question = questions[i-1]
                        question.correct_letter = request.POST.get(f'task5_question_{i}')
                        question.save()
                        # Обновляем варианты ответов
                        for letter in ['A', 'B', 'C']:
                            option_text = request.POST.get(f'task5_option{letter}_{i}')
                            option = question.options.filter(letter=letter).first()
                            if option:
                                option.text = option_text
                                option.save()
            
            return redirect('hsk2:listening_detail', pk=listening.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy('hsk2:listening_detail', kwargs={'pk': self.object.pk})

class ListeningDeleteView(DeleteView):
    model = ListeningHSK2
    template_name = 'hsk2/listening_confirm_delete.html'
    success_url = reverse_lazy('hsk2:listening_list')

### ЧТЕНИЕ

class ReadingListView(ListView):
    model = ReadingHSK2
    template_name = 'hsk2/reading_list.html'
    context_object_name = 'reading_variants'

class ReadingCreateView(CreateView):
    model = ReadingHSK2
    template_name = 'hsk2/reading_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант
            reading_var = ReadingHSK2.objects.create()
            
            # 2. Задание 1 (5 вопросов с текстом)
            task1_picture = request.POST.get('task1_picture_id')
            task1 = ReadingFirstTaskHSK2.objects.create(
                picture_id=task1_picture,
                reading_var=reading_var
            )

            for i in range(1, 6):
                text = request.POST.get(f'task1_text_{i}')
                correct_letter = request.POST.get(f'task1_question_{i}')
                ReadingFirstTaskHSK2Sentence.objects.create(
                    text=text,
                    correct_letter=correct_letter,
                    task=task1
                )
            
            # 3. Задание 2 (6 опций + 5 вопросов)
            task2 = ReadingSecondTaskHSK2.objects.create(reading_var=reading_var)
            # Опции задания 2
            for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                option_text = request.POST.get(f'task2_option_{letter}')
                ReadingSecondTaskHSK2Option.objects.create(
                    letter=letter,
                    text=option_text,
                    task=task2
                )
            # Вопросы задания 2
            for i in range(1, 6):
                text = request.POST.get(f'task2_text_{i}')
                correct_letter = request.POST.get(f'task2_question_{i}')
                ReadingSecondTaskHSK2Sentence.objects.create(
                    text=text,
                    correct_letter=correct_letter,
                    task=task2
                )
            
            # 4. Задание 3 (5 пар предложений)
            for i in range(1, 6):
                first_sentence = request.POST.get(f'task3_first_sentence_{i}')
                second_sentence = request.POST.get(f'task3_second_sentence_{i}')
                is_correct = request.POST.get(f'task3_question_{i}') == 'true'
                ReadingThirdTaskHSK2.objects.create(
                    first_sentence=first_sentence,
                    second_sentence=second_sentence,
                    is_correct=is_correct,
                    reading_var=reading_var
                )
            
            # 5. Задание 4 (6 опций + 5 вопросов)
            task4 = ReadingFourthTaskHSK2.objects.create(reading_var=reading_var)
            # Опции задания 4
            for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                option_text = request.POST.get(f'task4_option_{letter}')
                ReadingFourthTaskHSK2Option.objects.create(
                    letter=letter,
                    text=option_text,
                    task=task4
                )
            # Вопросы задания 4
            for i in range(1, 6):
                text = request.POST.get(f'task4_text_{i}')
                correct_letter = request.POST.get(f'task4_question_{i}')
                ReadingFourthTaskHSK2Question.objects.create(
                    text=text,
                    correct_letter=correct_letter,
                    task=task4
                )
            
            # 6. Задание 5 (5 опций + 5 вопросов) - используем ReadingFourthTaskHSK2
            task5 = ReadingFourthTaskHSK2.objects.create(reading_var=reading_var)
            # Опции задания 5
            for letter in ['A', 'B', 'C', 'D', 'E']:
                option_text = request.POST.get(f'task5_option_{letter}')
                ReadingFourthTaskHSK2Option.objects.create(
                    letter=letter,
                    text=option_text,
                    task=task5
                )
            # Вопросы задания 5
            for i in range(1, 6):
                text = request.POST.get(f'task5_text_{i}')
                correct_letter = request.POST.get(f'task5_question_{i}')
                ReadingFourthTaskHSK2Question.objects.create(
                    text=text,
                    correct_letter=correct_letter,
                    task=task5
                )
            
            return redirect('hsk2:reading_detail', pk=reading_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class ReadingDetailView(DetailView):
    model = ReadingHSK2
    template_name = 'hsk2/reading_detail.html'
    context_object_name = 'reading'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reading = self.object
        
        # Получаем все задания для отображения
        context['task1'] = reading.first_type_tasks.first()
        context['task2'] = reading.second_type_tasks.first()
        
        # Задание 3 - все объекты ThirdTaskHSK2
        context['task3_list'] = reading.third_type_tasks.all()
        
        # Для заданий 4 и 5 используем FourthTaskHSK2
        fourth_tasks = list(reading.fourth_type_tasks.all())
        if len(fourth_tasks) > 0:
            context['task4'] = fourth_tasks[0]  # Первое задание четвертого типа
        if len(fourth_tasks) > 1:
            context['task5'] = fourth_tasks[1]  # Второе задание четвертого типа
        
        return context

class ReadingUpdateView(UpdateView):
    model = ReadingHSK2
    template_name = 'hsk2/reading_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        reading = self.object
        context['reading'] = reading
        context['is_update'] = True
        
        # Задание 1
        task1 = reading.first_type_tasks.first()
        if task1:
            context['task1_picture_id'] = task1.picture_id
            context['task1_sentences'] = list(task1.sentences.all())
        
        # Задание 2
        task2 = reading.second_type_tasks.first()
        if task2:
            context['task2_options'] = {opt.letter: opt.text for opt in task2.options.all()}
            context['task2_sentences'] = list(task2.sentences.all())
        
        # Задание 3
        task3_list = list(reading.third_type_tasks.all())
        context['task3_list'] = task3_list
        
        # Задания 4 и 5 (FourthTaskHSK2)
        fourth_tasks = list(reading.fourth_type_tasks.all())
        if len(fourth_tasks) > 0:
            task4 = fourth_tasks[0]
            context['task4_options'] = {opt.letter: opt.text for opt in task4.options.all()}
            context['task4_questions'] = list(task4.questions.all())
        
        if len(fourth_tasks) > 1:
            task5 = fourth_tasks[1]
            context['task5_options'] = {opt.letter: opt.text for opt in task5.options.all()}
            context['task5_questions'] = list(task5.questions.all())
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        reading = self.object
        
        try:
            # 1. Обновляем Задание 1
            task1 = reading.first_type_tasks.first()
            if task1:
                task1.picture_id = request.POST.get('task1_picture_id')
                task1.save()
                # Обновляем предложения задания 1
                sentences = list(task1.sentences.all())
                for i in range(1, 6):
                    if i <= len(sentences):
                        sentences[i-1].text = request.POST.get(f'task1_text_{i}')
                        sentences[i-1].correct_letter = request.POST.get(f'task1_question_{i}')
                        sentences[i-1].save()
            
            # 2. Обновляем Задание 2
            task2 = reading.second_type_tasks.first()
            if task2:
                # Обновляем опции задания 2
                for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                    option_text = request.POST.get(f'task2_option_{letter}')
                    option = task2.options.filter(letter=letter).first()
                    if option:
                        option.text = option_text
                        option.save()
                
                # Обновляем предложения задания 2
                sentences = list(task2.sentences.all())
                for i in range(1, 6):
                    if i <= len(sentences):
                        sentences[i-1].text = request.POST.get(f'task2_text_{i}')
                        sentences[i-1].correct_letter = request.POST.get(f'task2_question_{i}')
                        sentences[i-1].save()
            
            # 3. Обновляем Задание 3
            task3_list = list(reading.third_type_tasks.all())
            for i in range(1, 6):
                if i <= len(task3_list):
                    task3 = task3_list[i-1]
                    task3.first_sentence = request.POST.get(f'task3_first_sentence_{i}')
                    task3.second_sentence = request.POST.get(f'task3_second_sentence_{i}')
                    task3.is_correct = request.POST.get(f'task3_question_{i}') == 'true'
                    task3.save()
            
            # 4. Обновляем Задание 4
            fourth_tasks = list(reading.fourth_type_tasks.all())
            if len(fourth_tasks) > 0:
                task4 = fourth_tasks[0]
                # Обновляем опции задания 4
                for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                    option_text = request.POST.get(f'task4_option_{letter}')
                    option = task4.options.filter(letter=letter).first()
                    if option:
                        option.text = option_text
                        option.save()
                
                # Обновляем вопросы задания 4
                questions = list(task4.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].text = request.POST.get(f'task4_text_{i}')
                        questions[i-1].correct_letter = request.POST.get(f'task4_question_{i}')
                        questions[i-1].save()
            
            # 5. Обновляем Задание 5
            if len(fourth_tasks) > 1:
                task5 = fourth_tasks[1]
                # Обновляем опции задания 5
                for letter in ['A', 'B', 'C', 'D', 'E']:
                    option_text = request.POST.get(f'task5_option_{letter}')
                    option = task5.options.filter(letter=letter).first()
                    if option:
                        option.text = option_text
                        option.save()
                
                # Обновляем вопросы задания 5
                questions = list(task5.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].text = request.POST.get(f'task5_text_{i}')
                        questions[i-1].correct_letter = request.POST.get(f'task5_question_{i}')
                        questions[i-1].save()
            
            return redirect('hsk2:reading_detail', pk=reading.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy('hsk2:reading_detail', kwargs={'pk': self.object.pk})

class ReadingDeleteView(DeleteView):
    model = ReadingHSK2
    template_name = 'hsk2/reading_confirm_delete.html'
    success_url = reverse_lazy('hsk2:reading_list')