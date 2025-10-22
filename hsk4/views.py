from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import *



def get_sections(request):
    return render(request, "hsk4/sections.html")


class ListeningListView(ListView):
    model = ListeningHSK4
    template_name = 'hsk4/hsk4_listening_list.html'
    context_object_name = 'listening_variants'

class ListeningCreateView(CreateView):
    model = ListeningHSK4
    template_name = 'hsk4/hsk4_listening_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант
            audio_id = request.POST.get('audio_id')
            listening_var = ListeningHSK4.objects.create(audio_id=audio_id)
            
            # 2. Задание 1 (10 boolean вопросов)
            for i in range(1, 11):
                text = request.POST.get(f'task1_text_{i}')
                is_correct = request.POST.get(f'task1_question_{i}') == 'true'
                FirstTaskHSK4.objects.create(
                    text=text,
                    is_correct=is_correct,
                    listening_var=listening_var
                )
            
            # 3. Задание 2 (15 вопросов с вариантами A-D)
            for i in range(1, 16):
                correct_letter = request.POST.get(f'task2_question_{i}')
                task2 = SecondTaskHSK4.objects.create(
                    correct_letter=correct_letter,
                    listening_var=listening_var
                )
                # Варианты ответов для задания 2
                for letter in ['A', 'B', 'C', 'D']:
                    option_text = request.POST.get(f'task2_option{letter}_{i}')
                    SecondTaskHSK4Option.objects.create(
                        letter=letter,
                        text=option_text,
                        task=task2
                    )
            
            # 4. Задание 3 (20 вопросов с вариантами A-D)
            for i in range(1, 21):
                correct_letter = request.POST.get(f'task3_question_{i}')
                task3 = ThirdTaskHSK4.objects.create(
                    correct_letter=correct_letter,
                    listening_var=listening_var
                )
                # Варианты ответов для задания 3
                for letter in ['A', 'B', 'C', 'D']:
                    option_text = request.POST.get(f'task3_option{letter}_{i}')
                    ThirdTaskHSK4Option.objects.create(
                        letter=letter,
                        text=option_text,
                        task=task3
                    )
            
            return redirect('hsk4:listening_detail', pk=listening_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class ListeningDetailView(DetailView):
    model = ListeningHSK4
    template_name = 'hsk4/hsk4_listening_detail.html'
    context_object_name = 'listening'

class ListeningUpdateView(UpdateView):
    model = ListeningHSK4
    template_name = 'hsk4/hsk4_listening_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        listening = self.object
        context['listening'] = listening
        context['is_update'] = True
        
        # Задание 1
        task1_list = list(listening.first_type_tasks.all())
        context['task1_list'] = task1_list
        
        # Задание 2
        task2_list = list(listening.second_type_tasks.all())
        context['task2_list'] = task2_list
        # Собираем варианты ответов для задания 2
        task2_options = {}
        for task2 in task2_list:
            task2_options[task2.id] = {opt.letter: opt.text for opt in task2.options.all()}
        context['task2_options'] = task2_options
        
        # Задание 3
        task3_list = list(listening.third_type_tasks.all())
        context['task3_list'] = task3_list
        # Собираем варианты ответов для задания 3
        task3_options = {}
        for task3 in task3_list:
            task3_options[task3.id] = {opt.letter: opt.text for opt in task3.options.all()}
        context['task3_options'] = task3_options
        
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
            task1_list = list(listening.first_type_tasks.all())
            for i in range(1, 11):
                if i <= len(task1_list):
                    task1 = task1_list[i-1]
                    task1.text = request.POST.get(f'task1_text_{i}')
                    task1.is_correct = request.POST.get(f'task1_question_{i}') == 'true'
                    task1.save()
            
            # 3. Обновляем Задание 2
            task2_list = list(listening.second_type_tasks.all())
            for i in range(1, 16):
                if i <= len(task2_list):
                    task2 = task2_list[i-1]
                    task2.correct_letter = request.POST.get(f'task2_question_{i}')
                    task2.save()
                    # Обновляем варианты ответов
                    for letter in ['A', 'B', 'C', 'D']:
                        option_text = request.POST.get(f'task2_option{letter}_{i}')
                        option = task2.options.filter(letter=letter).first()
                        if option:
                            option.text = option_text
                            option.save()
            
            # 4. Обновляем Задание 3
            task3_list = list(listening.third_type_tasks.all())
            for i in range(1, 21):
                if i <= len(task3_list):
                    task3 = task3_list[i-1]
                    task3.correct_letter = request.POST.get(f'task3_question_{i}')
                    task3.save()
                    # Обновляем варианты ответов
                    for letter in ['A', 'B', 'C', 'D']:
                        option_text = request.POST.get(f'task3_option{letter}_{i}')
                        option = task3.options.filter(letter=letter).first()
                        if option:
                            option.text = option_text
                            option.save()
            
            return redirect('hsk4:listening_detail', pk=listening.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy('hsk4:listening_detail', kwargs={'pk': self.object.pk})

class ListeningDeleteView(DeleteView):
    model = ListeningHSK4
    template_name = 'hsk4/hsk4_listening_confirm_delete.html'
    success_url = reverse_lazy('hsk4:listening_list')


### READING

class ReadingListView(ListView):
    model = ReadingHSK4
    template_name = 'hsk4/hsk4_reading_list.html'
    context_object_name = 'reading_variants'

class ReadingCreateView(CreateView):
    model = ReadingHSK4
    template_name = 'hsk4/hsk4_reading_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант
            reading_var = ReadingHSK4.objects.create()
            
            # 2. Задание 1 (6 опций A-F + 5 вопросов)
            task1 = ReadingFirstTaskHSK4.objects.create(reading_var=reading_var)
            # Опции задания 1
            for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                option_text = request.POST.get(f'task1_option_{letter}')
                ReadingFirstTaskOptionHSK4.objects.create(
                    letter=letter,
                    text=option_text,
                    task=task1
                )
            # Вопросы задания 1
            for i in range(1, 6):
                text = request.POST.get(f'task1_text_{i}')
                correct_letter = request.POST.get(f'task1_question_{i}')
                ReadingFirstTaskSentenceHSK4.objects.create(
                    text=text,
                    correct_letter=correct_letter,
                    task=task1
                )
            
            # 3. Задание 2 (6 опций A-F + 5 вопросов) - используем ReadingFirstTaskHSK4
            task2 = ReadingFirstTaskHSK4.objects.create(reading_var=reading_var)
            # Опции задания 2
            for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                option_text = request.POST.get(f'task2_option_{letter}')
                ReadingFirstTaskOptionHSK4.objects.create(
                    letter=letter,
                    text=option_text,
                    task=task2
                )
            # Вопросы задания 2
            for i in range(1, 6):
                text = request.POST.get(f'task2_text_{i}')
                correct_letter = request.POST.get(f'task2_question_{i}')
                ReadingFirstTaskSentenceHSK4.objects.create(
                    text=text,
                    correct_letter=correct_letter,
                    task=task2
                )
            
            # 4. Задание 3 (10 заданий с последовательностью)
            for i in range(1, 11):
                correct_sequence = request.POST.get(f'task3_sequence_{i}')
                task3 = ReadingSecondTaskHSK4.objects.create(
                    correct_sequence=correct_sequence,
                    reading_var=reading_var
                )
                # Опции для задания 3
                for letter in ['A', 'B', 'C']:
                    option_text = request.POST.get(f'task3_option{letter}_{i}')
                    ReadingSecondTaskOptionHSK4.objects.create(
                        letter=letter,
                        text=option_text,
                        task=task3
                    )
            
            # 5. Задание 4 (20 текстов с вопросами)
            for i in range(1, 16):
                text = request.POST.get(f'task4_text_{i}')
                task4 = ReadingThirdTaskHSK4.objects.create(
                    text=text,
                    reading_var=reading_var
                )
                # Вопрос для задания 4
                question_text = request.POST.get(f'task4_question_text_{i}')
                correct_letter = request.POST.get(f'task4_question_{i}')
                question = ReadingThirdTaskQuestionHSK4.objects.create(
                    text=question_text,
                    correct_letter=correct_letter,
                    task=task4
                )
                # Варианты ответов для задания 4
                for letter in ['A', 'B', 'C', 'D']:
                    option_text = request.POST.get(f'task4_option{letter}_{i}')
                    QuestionOptionHSK4.objects.create(
                        letter=letter,
                        text=option_text,
                        question=question
                    )
            
            # 6. Задание 5 (3 текста по 2 вопроса) - используем ReadingThirdTaskHSK4
            for i in range(1, 4):
                text = request.POST.get(f'task5_text_{i}')
                task5 = ReadingThirdTaskHSK4.objects.create(
                    text=text,
                    reading_var=reading_var
                )
                # 2 вопроса для каждого текста
                for j in range(1, 3):
                    question_text = request.POST.get(f'task5_question_text_{i}_{j}')
                    correct_letter = request.POST.get(f'task5_question_{i}_{j}')
                    question = ReadingThirdTaskQuestionHSK4.objects.create(
                        text=question_text,
                        correct_letter=correct_letter,
                        task=task5
                    )
                    # Варианты ответов для вопроса
                    for letter in ['A', 'B', 'C', 'D']:
                        option_text = request.POST.get(f'task5_option{letter}_{i}_{j}')
                        QuestionOptionHSK4.objects.create(
                            letter=letter,
                            text=option_text,
                            question=question
                        )
            
            return redirect('hsk4:reading_detail', pk=reading_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class ReadingDetailView(DetailView):
    model = ReadingHSK4
    template_name = 'hsk4/hsk4_reading_detail.html'
    context_object_name = 'reading'

class ReadingUpdateView(UpdateView):
    model = ReadingHSK4
    template_name = 'hsk4/hsk4_reading_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        reading = self.object
        context['reading'] = reading
        context['is_update'] = True
        
        # Задания 1 и 2 (ReadingFirstTaskHSK4)
        first_tasks = list(reading.first_type_tasks.all())
        if len(first_tasks) > 0:
            context['task1'] = first_tasks[0]
        if len(first_tasks) > 1:
            context['task2'] = first_tasks[1]
        
        # Задание 3 (ReadingSecondTaskHSK4)
        second_tasks = list(reading.second_type_tasks.all())
        context['task3_list'] = second_tasks
        
        # Задания 4 и 5 (ReadingThirdTaskHSK4)
        third_tasks = list(reading.third_type_tasks.all())
        context['task4_list'] = third_tasks[:20]  # Первые 20 - задание 4
        context['task5_list'] = third_tasks[20:23]  # Следующие 3 - задание 5
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        reading = self.object
        
        try:
            # 1. Обновляем Задание 1
            first_tasks = list(reading.first_type_tasks.all())
            if len(first_tasks) > 0:
                task1 = first_tasks[0]
                # Обновляем опции задания 1
                for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                    option_text = request.POST.get(f'task1_option_{letter}')
                    option = task1.options.filter(letter=letter).first()
                    if option:
                        option.text = option_text
                        option.save()
                # Обновляем вопросы задания 1
                sentences = list(task1.sentences.all())
                for i in range(1, 6):
                    if i <= len(sentences):
                        sentences[i-1].text = request.POST.get(f'task1_text_{i}')
                        sentences[i-1].correct_letter = request.POST.get(f'task1_question_{i}')
                        sentences[i-1].save()
            
            # 2. Обновляем Задание 2
            if len(first_tasks) > 1:
                task2 = first_tasks[1]
                # Обновляем опции задания 2
                for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                    option_text = request.POST.get(f'task2_option_{letter}')
                    option = task2.options.filter(letter=letter).first()
                    if option:
                        option.text = option_text
                        option.save()
                # Обновляем вопросы задания 2
                sentences = list(task2.sentences.all())
                for i in range(1, 6):
                    if i <= len(sentences):
                        sentences[i-1].text = request.POST.get(f'task2_text_{i}')
                        sentences[i-1].correct_letter = request.POST.get(f'task2_question_{i}')
                        sentences[i-1].save()
            
            # 3. Обновляем Задание 3
            second_tasks = list(reading.second_type_tasks.all())
            for i in range(1, 11):
                if i <= len(second_tasks):
                    task3 = second_tasks[i-1]
                    task3.correct_sequence = request.POST.get(f'task3_sequence_{i}')
                    task3.save()
                    # Обновляем опции
                    for letter in ['A', 'B', 'C']:
                        option_text = request.POST.get(f'task3_option{letter}_{i}')
                        option = task3.options.filter(letter=letter).first()
                        if option:
                            option.text = option_text
                            option.save()
            
            # 4. Обновляем Задание 4
            third_tasks = list(reading.third_type_tasks.all())
            for i in range(1, 16):
                if i <= len(third_tasks):
                    task4 = third_tasks[i-1]
                    task4.text = request.POST.get(f'task4_text_{i}')
                    task4.save()
                    # Обновляем вопрос
                    questions = list(task4.questions.all())
                    if len(questions) > 0:
                        question = questions[0]
                        question.text = request.POST.get(f'task4_question_text_{i}')
                        question.correct_letter = request.POST.get(f'task4_question_{i}')
                        question.save()
                        # Обновляем варианты ответов
                        for letter in ['A', 'B', 'C', 'D']:
                            option_text = request.POST.get(f'task4_option{letter}_{i}')
                            option = question.options.filter(letter=letter).first()
                            if option:
                                option.text = option_text
                                option.save()
            
            # 5. Обновляем Задание 5
            for i in range(1, 4):
                task_index = 20 + i - 1  # task5_1 -> index 20, task5_2 -> index 21, task5_3 -> index 22
                if task_index < len(third_tasks):
                    task5 = third_tasks[task_index]
                    task5.text = request.POST.get(f'task5_text_{i}')
                    task5.save()
                    # Обновляем вопросы
                    questions = list(task5.questions.all())
                    for j in range(1, 3):
                        if j <= len(questions):
                            question = questions[j-1]
                            question.text = request.POST.get(f'task5_question_text_{i}_{j}')
                            question.correct_letter = request.POST.get(f'task5_question_{i}_{j}')
                            question.save()
                            # Обновляем варианты ответов
                            for letter in ['A', 'B', 'C', 'D']:
                                option_text = request.POST.get(f'task5_option{letter}_{i}_{j}')
                                option = question.options.filter(letter=letter).first()
                                if option:
                                    option.text = option_text
                                    option.save()
            
            return redirect('hsk4:reading_detail', pk=reading.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy('hsk4:reading_detail', kwargs={'pk': self.object.pk})

class ReadingDeleteView(DeleteView):
    model = ReadingHSK4
    template_name = 'hsk4/hsk4_reading_confirm_delete.html'
    success_url = reverse_lazy('hsk4:reading_list')

### WRITING

class WritingListView(ListView):
    model = WritingHSK4
    template_name = 'hsk4/hsk4_writing_list.html'
    context_object_name = 'writing_variants'

class WritingCreateView(CreateView):
    model = WritingHSK4
    template_name = 'hsk4/hsk4_writing_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант
            writing_var = WritingHSK4.objects.create()
            
            # 2. Задание 1 (10 заданий на составление предложений)
            for i in range(1, 11):
                words = request.POST.get(f'task1_words_{i}')
                correct_sentence = request.POST.get(f'task1_answer_{i}')
                if words and correct_sentence:
                    WritingFirstTaskHSK4.objects.create(
                        words=words.strip(),
                        correct_sentence=correct_sentence.strip(),
                        writing_var=writing_var
                    )
            
            # 3. Задание 2 (1 картинка + 5 слов-заданий)
            picture_id = request.POST.get('task2_picture')
            if picture_id:
                second_task = WritingSecondTaskHSK4.objects.create(
                    picture_id=picture_id.strip(),
                    writing_var=writing_var
                )
                
                # Добавляем 5 слов для этого задания
                for j in range(1, 6):
                    word_text = request.POST.get(f'task2_word_{j}')
                    word_answer = request.POST.get(f'task2_word_answer_{j}')
                    if word_text and word_answer:
                        WritingSecondTaskWord.objects.create(
                            text=word_text.strip(),
                            possible_answer=word_answer.strip(),
                            task=second_task
                        )
            
            return redirect('hsk4:writing_detail', pk=writing_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class WritingUpdateView(UpdateView):
    model = WritingHSK4
    template_name = 'hsk4/hsk4_writing_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        writing = self.object
        context['writing'] = writing
        context['is_update'] = True
        
        # Задание 1 (WritingFirstTaskHSK4)
        task1_list = list(writing.first_type_tasks.all())
        context['task1_list'] = task1_list
        
        # Задание 2 (WritingSecondTaskHSK4) - берем первую запись
        task2_list = list(writing.second_type_tasks.all())
        context['task2_list'] = task2_list
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        writing = self.object
        
        try:
            # 1. Обновляем Задание 1 (10 заданий)
            task1_list = list(writing.first_type_tasks.all())
            for i in range(1, 11):
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
                        WritingFirstTaskHSK4.objects.create(
                            words=words.strip(),
                            correct_sentence=correct_sentence.strip(),
                            writing_var=writing
                        )
            
            # 2. Обновляем Задание 2 (1 картинка + 5 слов)
            task2_list = list(writing.second_type_tasks.all())
            if task2_list:
                task2 = task2_list[0]
                task2.picture_id = request.POST.get('task2_picture')
                task2.save()
                
                # Обновляем слова для этого задания
                word_list = list(task2.words.all())
                for j in range(1, 6):
                    if j <= len(word_list):
                        word = word_list[j-1]
                        word.text = request.POST.get(f'task2_word_{j}')
                        word.possible_answer = request.POST.get(f'task2_word_answer_{j}')
                        word.save()
                    else:
                        # Если слова не существовало, создаем новое
                        word_text = request.POST.get(f'task2_word_{j}')
                        word_answer = request.POST.get(f'task2_word_answer_{j}')
                        if word_text and word_answer:
                            WritingSecondTaskWord.objects.create(
                                text=word_text.strip(),
                                possible_answer=word_answer.strip(),
                                task=task2
                            )
            else:
                # Если задания не существовало, создаем новое
                picture_id = request.POST.get('task2_picture')
                if picture_id:
                    new_task = WritingSecondTaskHSK4.objects.create(
                        picture_id=picture_id.strip(),
                        writing_var=writing
                    )
                    
                    # Добавляем слова для нового задания
                    for j in range(1, 6):
                        word_text = request.POST.get(f'task2_word_{j}')
                        word_answer = request.POST.get(f'task2_word_answer_{j}')
                        if word_text and word_answer:
                            WritingSecondTaskWord.objects.create(
                                text=word_text.strip(),
                                possible_answer=word_answer.strip(),
                                task=new_task
                            )
            
            return redirect('hsk4:writing_detail', pk=writing.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)

class WritingDetailView(DetailView):
    model = WritingHSK4
    template_name = 'hsk4/hsk4_writing_detail.html'
    context_object_name = 'writing'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        writing = self.object
        
        # Получаем все задания для отображения
        context['task1_list'] = writing.first_type_tasks.all()
        context['task2_list'] = writing.second_type_tasks.all()
        
        # Считаем общее количество слов для заданий 2 типа
        total_words = 0
        for task in writing.second_type_tasks.all():
            total_words += task.words.count()
        context['total_words'] = total_words
        
        return context


class WritingDeleteView(DeleteView):
    model = WritingHSK4
    template_name = 'hsk4/hsk4_writing_confirm_delete.html'
    success_url = reverse_lazy('hsk4:writing_list')