from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import *



def get_sections(request):
    return render(request, "hsk5/sections.html")

class ListeningListView(ListView):
    model = ListeningHSK5
    template_name = 'hsk5/hsk5_listening_list.html'
    context_object_name = 'writing_variants'  # Оставляем как в шаблоне
    
    def get_queryset(self):
        return ListeningHSK5.objects.all().order_by('-id')

class ListeningDetailView(DetailView):
    model = ListeningHSK5
    template_name = 'hsk5/hsk5_listening_detail.html'
    context_object_name = 'listening'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listening = self.object
        
        # Разделяем задания: первые 20 - задание 1, остальные - задание 2
        all_tasks = list(listening.first_type_tasks.all())
        
        # Задание 1 - первые 20 вопросов
        context['task1_list'] = all_tasks[:20]
        # Задание 2 - следующие 25 вопросов
        context['task2_list'] = all_tasks[20:45]
        
        return context

class ListeningCreateView(CreateView):
    model = ListeningHSK5
    template_name = 'hsk5/hsk5_listening_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант с audio_id
            audio_id = request.POST.get('audio_id')
            listening_var = ListeningHSK5.objects.create(audio_id=audio_id.strip())
            
            # 2. Задание 1 (20 вопросов)
            for i in range(1, 21):
                correct_letter = request.POST.get(f'task1_correct_{i}')
                if correct_letter:
                    task = FirstTaskHSK5.objects.create(
                        correct_letter=correct_letter.strip().upper(),
                        listening_var=listening_var
                    )
                    
                    # Создаем 4 варианта ответов (A, B, C, D)
                    for letter in "ABCD":
                        option_text = request.POST.get(f'task1_option_{i}_{letter}')
                        if option_text:
                            FirstTaskHSK5Option.objects.create(
                                letter=letter,
                                text=option_text.strip(),
                                task=task
                            )
            
            # 3. Задание 2 (25 вопросов) - сохраняем в ту же модель
            for i in range(1, 26):
                correct_letter = request.POST.get(f'task2_correct_{i}')
                if correct_letter:
                    task = FirstTaskHSK5.objects.create(
                        correct_letter=correct_letter.strip().upper(),
                        listening_var=listening_var
                    )
                    
                    # Создаем 4 варианта ответов (A, B, C, D)
                    for letter in "ABCD":
                        option_text = request.POST.get(f'task2_option_{i}_{letter}')
                        if option_text:
                            FirstTaskHSK5Option.objects.create(
                                letter=letter,
                                text=option_text.strip(),
                                task=task
                            )
            
            return redirect('hsk5:listening_detail', pk=listening_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class ListeningUpdateView(UpdateView):
    model = ListeningHSK5
    template_name = 'hsk5/hsk5_listening_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        listening = self.object
        context['listening'] = listening
        context['is_update'] = True
        
        # Получаем все задания и разделяем их
        all_tasks = list(listening.first_type_tasks.all())
        context['task1_list'] = all_tasks[:20]  # Первые 20 - задание 1
        context['task2_list'] = all_tasks[20:45]  # Следующие 25 - задание 2
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        listening = self.object
        
        try:
            # Обновляем audio_id
            listening.audio_id = request.POST.get('audio_id')
            listening.save()
            
            all_tasks = list(listening.first_type_tasks.all())
            
            # Обновляем Задание 1 (20 вопросов)
            for i in range(1, 21):
                correct_letter = request.POST.get(f'task1_correct_{i}')
                if i <= len(all_tasks):
                    task = all_tasks[i-1]
                    task.correct_letter = correct_letter.strip().upper()
                    task.save()
                else:
                    # Создаем новое задание, если не существует
                    if correct_letter:
                        task = FirstTaskHSK5.objects.create(
                            correct_letter=correct_letter.strip().upper(),
                            listening_var=listening
                        )
                        all_tasks.append(task)
                
                # Обновляем варианты ответов для задания 1
                if i <= len(all_tasks):
                    task = all_tasks[i-1]
                    options_dict = {opt.letter: opt for opt in task.options.all()}
                    
                    for letter in "ABCD":
                        option_text = request.POST.get(f'task1_option_{i}_{letter}')
                        if letter in options_dict:
                            # Обновляем существующий вариант
                            option = options_dict[letter]
                            option.text = option_text.strip()
                            option.save()
                        else:
                            # Создаем новый вариант
                            if option_text:
                                FirstTaskHSK5Option.objects.create(
                                    letter=letter,
                                    text=option_text.strip(),
                                    task=task
                                )
            
            # Обновляем Задание 2 (25 вопросов)
            for i in range(1, 26):
                task_index = 20 + i - 1  # Индекс в общем списке
                correct_letter = request.POST.get(f'task2_correct_{i}')
                
                if task_index < len(all_tasks):
                    task = all_tasks[task_index]
                    task.correct_letter = correct_letter.strip().upper()
                    task.save()
                else:
                    # Создаем новое задание, если не существует
                    if correct_letter:
                        task = FirstTaskHSK5.objects.create(
                            correct_letter=correct_letter.strip().upper(),
                            listening_var=listening
                        )
                        all_tasks.append(task)
                
                # Обновляем варианты ответов для задания 2
                if task_index < len(all_tasks):
                    task = all_tasks[task_index]
                    options_dict = {opt.letter: opt for opt in task.options.all()}
                    
                    for letter in "ABCD":
                        option_text = request.POST.get(f'task2_option_{i}_{letter}')
                        if letter in options_dict:
                            # Обновляем существующий вариант
                            option = options_dict[letter]
                            option.text = option_text.strip()
                            option.save()
                        else:
                            # Создаем новый вариант
                            if option_text:
                                FirstTaskHSK5Option.objects.create(
                                    letter=letter,
                                    text=option_text.strip(),
                                    task=task
                                )
            
            return redirect('hsk5:listening_detail', pk=listening.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)

class ListeningDeleteView(DeleteView):
    model = ListeningHSK5
    template_name = 'hsk5/hsk5_listening_confirm_delete.html'
    success_url = reverse_lazy('hsk5:listening_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listening = self.object
        
        all_tasks = listening.first_type_tasks.all()
        task1_count = min(20, all_tasks.count())
        task2_count = max(0, all_tasks.count() - 20)
        
        context['task1_count'] = task1_count
        context['task2_count'] = task2_count
        context['total_questions'] = all_tasks.count()
        
        return context
    
### READING

class ReadingListView(ListView):
    model = ReadingHSK5
    template_name = 'hsk5/hsk5_reading_list.html'
    context_object_name = 'reading_variants'
    
    def get_queryset(self):
        return ReadingHSK5.objects.all().order_by('-id')

class ReadingDetailView(DetailView):
    model = ReadingHSK5
    template_name = 'hsk5/hsk5_reading_detail.html'
    context_object_name = 'reading'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reading = self.object
        
        context['task1_list'] = reading.first_type_tasks.all()
        context['task2_list'] = reading.second_type_tasks.all()
        context['task3_list'] = reading.third_type_tasks.all()
        
        return context

class ReadingCreateView(CreateView):
    model = ReadingHSK5
    template_name = 'hsk5/hsk5_reading_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант
            reading_var = ReadingHSK5.objects.create()
            
            # 2. Задание 1 (4 текста с вопросами)
            # Первый текст (3 вопроса)
            task1_text_1 = request.POST.get('task1_text_1')
            if task1_text_1:
                task1_1 = ReadingFirstTaskHSK5.objects.create(
                    text=task1_text_1.strip(),
                    reading_var=reading_var
                )
                # Создаем 3 вопроса для первого текста
                for j in range(3):
                    question_text = request.POST.get(f'task1_question_1_{j+1}')
                    correct_letter = request.POST.get(f'task1_correct_1_{j+1}')
                    if question_text and correct_letter:
                        question = ReadingFirstTaskHSK5Question.objects.create(
                            text=question_text.strip(),
                            correct_letter=correct_letter.strip().upper(),
                            task=task1_1
                        )
                        # Создаем варианты ответов для вопроса
                        for letter in "ABCD":
                            option_text = request.POST.get(f'task1_option_1_{j+1}_{letter}')
                            if option_text:
                                ReadingFirstTaskQuestionOptionHSK5.objects.create(
                                    letter=letter,
                                    text=option_text.strip(),
                                    question=question
                                )
            
            # Тексты 2-4 (по 4 вопроса)
            for i in range(2, 5):
                task_text = request.POST.get(f'task1_text_{i}')
                if task_text:
                    task = ReadingFirstTaskHSK5.objects.create(
                        text=task_text.strip(),
                        reading_var=reading_var
                    )
                    # Создаем 4 вопроса для текста
                    for j in range(4):
                        question_text = request.POST.get(f'task1_question_{i}_{j+1}')
                        correct_letter = request.POST.get(f'task1_correct_{i}_{j+1}')
                        if question_text and correct_letter:
                            question = ReadingFirstTaskHSK5Question.objects.create(
                                text=question_text.strip(),
                                correct_letter=correct_letter.strip().upper(),
                                task=task
                            )
                            # Создаем варианты ответов для вопроса
                            for letter in "ABCD":
                                option_text = request.POST.get(f'task1_option_{i}_{j+1}_{letter}')
                                if option_text:
                                    ReadingFirstTaskQuestionOptionHSK5.objects.create(
                                        letter=letter,
                                        text=option_text.strip(),
                                        question=question
                                    )
            
            # 3. Задание 2 (10 вопросов)
            for i in range(1, 11):
                task_text = request.POST.get(f'task2_text_{i}')
                correct_letter = request.POST.get(f'task2_correct_{i}')
                if task_text and correct_letter:
                    task = ReadingSecondTaskHSK5.objects.create(
                        text=task_text.strip(),
                        correct_letter=correct_letter.strip().upper(),
                        reading_var=reading_var
                    )
                    # Создаем варианты ответов
                    for letter in "ABCD":
                        option_text = request.POST.get(f'task2_option_{i}_{letter}')
                        if option_text:
                            ReadingSecondTaskHSK5Option.objects.create(
                                letter=letter,
                                text=option_text.strip(),
                                task=task
                            )
            
            for i in range(1, 6):
                task3_text = request.POST.get(f'task3_text_{i}')
                task3_photo_id = request.POST.get(f'task3_photo_id_{i}')
                if task3_text:
                    task3 = ReadingThirdTaskHSK5.objects.create(
                        text=task3_text.strip(),
                        photo_id=task3_photo_id.strip() if task3_photo_id else None,
                        reading_var=reading_var
                    )
                    
                    # Создаем вопросы для задания 3
                    question_index = 0
                    while True:
                        question_text = request.POST.get(f'task3_question_{i}_{question_index}')
                        if not question_text:
                            break
                        
                        correct_letter = request.POST.get(f'task3_correct_{i}_{question_index}')
                        if question_text and correct_letter:
                            question = ReadingThirdTaskHSK5Question.objects.create(
                                text=question_text.strip(),
                                correct_letter=correct_letter.strip().upper(),
                                task=task3
                            )
                            # Создаем варианты ответов для вопроса
                            for letter in "ABCD":
                                option_text = request.POST.get(f'task3_option_{i}_{question_index}_{letter}')
                                if option_text:
                                    ReadingThirdTaskQuestionOptionHSK5.objects.create(
                                        letter=letter,
                                        text=option_text.strip(),
                                        question=question
                                    )
                        
                        question_index += 1
            
            return redirect('hsk5:reading_detail', pk=reading_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class ReadingUpdateView(UpdateView):
    model = ReadingHSK5
    template_name = 'hsk5/hsk5_reading_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        reading = self.object
        context['reading'] = reading
        context['is_update'] = True
        
        context['task1_list'] = list(reading.first_type_tasks.all())
        context['task2_list'] = list(reading.second_type_tasks.all())
        context['task3_list'] = list(reading.third_type_tasks.all())
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        reading = self.object
        
        try:
            # 1. Обновляем Задание 1
            task1_list = list(reading.first_type_tasks.all())
            
            # Первый текст (3 вопроса)
            if len(task1_list) > 0:
                task1_1 = task1_list[0]
                task1_1.text = request.POST.get('task1_text_1')
                task1_1.save()
                
                # Обновляем вопросы для первого текста
                questions_1 = list(task1_1.questions.all())
                for j in range(3):
                    if j < len(questions_1):
                        question = questions_1[j]
                        question.text = request.POST.get(f'task1_question_1_{j+1}')
                        question.correct_letter = request.POST.get(f'task1_correct_1_{j+1}').upper()
                        question.save()
                        
                        # Обновляем варианты ответов
                        options_dict = {opt.letter: opt for opt in question.options.all()}
                        for letter in "ABCD":
                            option_text = request.POST.get(f'task1_option_1_{j+1}_{letter}')
                            if letter in options_dict:
                                option = options_dict[letter]
                                option.text = option_text
                                option.save()
            
            # Тексты 2-4 (по 4 вопроса)
            for i in range(2, 5):
                task_index = i - 1
                if task_index < len(task1_list):
                    task = task1_list[task_index]
                    task.text = request.POST.get(f'task1_text_{i}')
                    task.save()
                    
                    # Обновляем вопросы
                    questions = list(task.questions.all())
                    for j in range(4):
                        if j < len(questions):
                            question = questions[j]
                            question.text = request.POST.get(f'task1_question_{i}_{j+1}')
                            question.correct_letter = request.POST.get(f'task1_correct_{i}_{j+1}').upper()
                            question.save()
                            
                            # Обновляем варианты ответов
                            options_dict = {opt.letter: opt for opt in question.options.all()}
                            for letter in "ABCD":
                                option_text = request.POST.get(f'task1_option_{i}_{j+1}_{letter}')
                                if letter in options_dict:
                                    option = options_dict[letter]
                                    option.text = option_text
                                    option.save()
            
            # 2. Обновляем Задание 2
            task2_list = list(reading.second_type_tasks.all())
            for i in range(1, 11):
                if i <= len(task2_list):
                    task = task2_list[i-1]
                    task.text = request.POST.get(f'task2_text_{i}')
                    task.correct_letter = request.POST.get(f'task2_correct_{i}').upper()
                    task.save()
                    
                    # Обновляем варианты ответов
                    options_dict = {opt.letter: opt for opt in task.options.all()}
                    for letter in "ABCD":
                        option_text = request.POST.get(f'task2_option_{i}_{letter}')
                        if letter in options_dict:
                            option = options_dict[letter]
                            option.text = option_text
                            option.save()
            
            # 3. Обновляем Задание 3
            task3_list = list(reading.third_type_tasks.all())
            for i in range(1, 6):
                if i <= len(task3_list):
                    task3 = task3_list[i-1]
                    task3.text = request.POST.get(f'task3_text_{i}')
                    task3.photo_id = request.POST.get(f'task3_photo_id_{i}') or None
                    task3.save()
                    
                    # Удаляем старые вопросы и создаем новые
                    task3.questions.all().delete()
                    
                    question_index = 0
                    while True:
                        question_text = request.POST.get(f'task3_question_{i}_{question_index}')
                        if not question_text:
                            break
                        
                        correct_letter = request.POST.get(f'task3_correct_{i}_{question_index}')
                        if question_text and correct_letter:
                            question = ReadingThirdTaskHSK5Question.objects.create(
                                text=question_text.strip(),
                                correct_letter=correct_letter.strip().upper(),
                                task=task3
                            )
                            # Создаем варианты ответов для вопроса
                            for letter in "ABCD":
                                option_text = request.POST.get(f'task3_option_{i}_{question_index}_{letter}')
                                if option_text:
                                    ReadingThirdTaskQuestionOptionHSK5.objects.create(
                                        letter=letter,
                                        text=option_text.strip(),
                                        question=question
                                    )
                        
                        question_index += 1
                else:
                    # Создаем новый текст, если не существует
                    task3_text = request.POST.get(f'task3_text_{i}')
                    task3_photo_id = request.POST.get(f'task3_photo_id_{i}')
                    if task3_text:
                        task3 = ReadingThirdTaskHSK5.objects.create(
                            text=task3_text.strip(),
                            photo_id=task3_photo_id.strip() if task3_photo_id else None,
                            reading_var=reading
                        )
                        
                        # Создаем вопросы для нового текста
                        question_index = 0
                        while True:
                            question_text = request.POST.get(f'task3_question_{i}_{question_index}')
                            if not question_text:
                                break
                            
                            correct_letter = request.POST.get(f'task3_correct_{i}_{question_index}')
                            if question_text and correct_letter:
                                question = ReadingThirdTaskHSK5Question.objects.create(
                                    text=question_text.strip(),
                                    correct_letter=correct_letter.strip().upper(),
                                    task=task3
                                )
                                # Создаем варианты ответов для вопроса
                                for letter in "ABCD":
                                    option_text = request.POST.get(f'task3_option_{i}_{question_index}_{letter}')
                                    if option_text:
                                        ReadingThirdTaskQuestionOptionHSK5.objects.create(
                                            letter=letter,
                                            text=option_text.strip(),
                                            question=question
                                        )
                            
                            question_index += 1
            
            return redirect('hsk5:reading_detail', pk=reading.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)

class ReadingDeleteView(DeleteView):
    model = ReadingHSK5
    template_name = 'hsk5/hsk5_reading_confirm_delete.html'
    success_url = reverse_lazy('hsk5:reading_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reading = self.object
        
        # Считаем общее количество вопросов
        total_questions = 0
        for task in reading.first_type_tasks.all():
            total_questions += task.questions.count()
        total_questions += reading.second_type_tasks.count()
        for task in reading.third_type_tasks.all():
            total_questions += task.questions.count()
        
        context['task1_count'] = reading.first_type_tasks.count()
        context['task2_count'] = reading.second_type_tasks.count()
        context['task3_count'] = reading.third_type_tasks.count()
        context['total_questions'] = total_questions
        
        return context
    
### WRITING

class WritingListView(ListView):
    model = WritingHSK5
    template_name = 'hsk5/hsk5_writing_list.html'
    context_object_name = 'writing_variants'
    
    def get_queryset(self):
        return WritingHSK5.objects.all().order_by('-id')

class WritingDetailView(DetailView):
    model = WritingHSK5
    template_name = 'hsk5/hsk5_writing_detail.html'
    context_object_name = 'writing'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        writing = self.object
        
        context['task1_list'] = writing.first_type_tasks.all()
        context['task2_list'] = writing.second_type_tasks.all()
        context['task3_list'] = writing.third_type_tasks.all()
        
        return context

class WritingCreateView(CreateView):
    model = WritingHSK5
    template_name = 'hsk5/hsk5_writing_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант
            writing_var = WritingHSK5.objects.create()
            
            # 2. Задание 1 (8 заданий на составление предложений)
            for i in range(1, 9):
                words = request.POST.get(f'task1_words_{i}')
                correct_sentence = request.POST.get(f'task1_answer_{i}')
                if words and correct_sentence:
                    WritingFirstTaskHSK5.objects.create(
                        words=words.strip(),
                        correct_sentence=correct_sentence.strip(),
                        writing_var=writing_var
                    )
            
            # 3. Задание 2 (написание по тексту)
            task2_text = request.POST.get('task2_text')
            if task2_text:
                WritingSecondTaskHSK5.objects.create(
                    text=task2_text.strip(),
                    writing_var=writing_var
                )
            
            # 4. Задание 3 (описание картинки)
            task3_picture_id = request.POST.get('task3_picture_id')
            if task3_picture_id:
                WritingThirdTaskHSK5.objects.create(
                    picture_id=task3_picture_id.strip(),
                    writing_var=writing_var
                )
            
            return redirect('hsk5:writing_detail', pk=writing_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class WritingUpdateView(UpdateView):
    model = WritingHSK5
    template_name = 'hsk5/hsk5_writing_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        writing = self.object
        context['writing'] = writing
        context['is_update'] = True
        
        context['task1_list'] = list(writing.first_type_tasks.all())
        context['task2_list'] = list(writing.second_type_tasks.all())
        context['task3_list'] = list(writing.third_type_tasks.all())
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        writing = self.object
        
        try:
            # 1. Обновляем Задание 1 (8 заданий)
            task1_list = list(writing.first_type_tasks.all())
            for i in range(1, 9):
                if i <= len(task1_list):
                    task1 = task1_list[i-1]
                    task1.words = request.POST.get(f'task1_words_{i}')
                    task1.correct_sentence = request.POST.get(f'task1_answer_{i}')
                    task1.save()
                else:
                    # Если задания не существовало, создаем новое
                    words = request.POST.get(f'task1_words_{i}')
                    correct_sentence = request.POST.get(f'task1_answer_{i}')
                    if words and correct_sentence:
                        WritingFirstTaskHSK5.objects.create(
                            words=words.strip(),
                            correct_sentence=correct_sentence.strip(),
                            writing_var=writing
                        )
            
            # 2. Обновляем Задание 2 (написание по тексту)
            task2_list = list(writing.second_type_tasks.all())
            task2_text = request.POST.get('task2_text')
            if task2_list:
                task2 = task2_list[0]
                task2.text = task2_text.strip()
                task2.save()
            else:
                # Если задания не существовало, создаем новое
                if task2_text:
                    WritingSecondTaskHSK5.objects.create(
                        text=task2_text.strip(),
                        writing_var=writing
                    )
            
            # 3. Обновляем Задание 3 (описание картинки)
            task3_list = list(writing.third_type_tasks.all())
            task3_picture_id = request.POST.get('task3_picture_id')
            if task3_list:
                task3 = task3_list[0]
                task3.picture_id = task3_picture_id.strip()
                task3.save()
            else:
                # Если задания не существовало, создаем новое
                if task3_picture_id:
                    WritingThirdTaskHSK5.objects.create(
                        picture_id=task3_picture_id.strip(),
                        writing_var=writing
                    )
            
            return redirect('hsk5:writing_detail', pk=writing.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)

class WritingDeleteView(DeleteView):
    model = WritingHSK5
    template_name = 'hsk5/hsk5_writing_confirm_delete.html'
    success_url = reverse_lazy('hsk5:writing_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        writing = self.object
        
        context['task1_count'] = writing.first_type_tasks.count()
        context['task2_count'] = writing.second_type_tasks.count()
        context['task3_count'] = writing.third_type_tasks.count()
        
        return context