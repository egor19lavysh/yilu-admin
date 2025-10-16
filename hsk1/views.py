from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ListeningHSK1
from hsk1.models import *


### АУДИРОВАНИЕ

def get_sections(request):
    return render(request, "hsk1/sections.html")


class ListeningListView(ListView):
    model = ListeningHSK1
    template_name = 'hsk1/listening_list.html'
    context_object_name = 'listening_variants'

class ListeningCreateView(CreateView):
    model = ListeningHSK1
    template_name = 'hsk1/create_listening.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            audio_id = request.POST.get('audio_id')
            listening_var = ListeningHSK1.objects.create(audio_id=audio_id)
            
            task1_picture = request.POST.get('task1_picture_id')
            task1 = FirstTaskHSK1.objects.create(
                picture_id=task1_picture,
                listening_var=listening_var
            )
            for i in range(1, 6):
                is_correct = request.POST.get(f'task1_question_{i}') == 'true'
                FirstTaskHSK1Question.objects.create(
                    is_correct=is_correct,
                    task=task1
                )
            
            task2_picture = request.POST.get('task2_picture_id')
            task2 = SecondTaskHSK1.objects.create(
                picture_id=task2_picture,
                listening_var=listening_var
            )
            for i in range(1, 6):
                correct_letter = request.POST.get(f'task2_question_{i}')
                SecondTaskHSK1Question.objects.create(
                    correct_letter=correct_letter,
                    task=task2
                )
            
            task3_picture = request.POST.get('task3_picture_id')
            task3 = ThirdTaskHSK1.objects.create(
                picture_id=task3_picture,
                listening_var=listening_var
            )
            for i in range(1, 6):
                correct_letter = request.POST.get(f'task3_question_{i}')
                ThirdTaskHSK1Question.objects.create(
                    correct_letter=correct_letter,
                    task=task3
                )
            
            task4 = FourthTaskHSK1.objects.create(listening_var=listening_var)
            for i in range(1, 6):
                correct_letter = request.POST.get(f'task4_question_{i}')
                question = FourthTaskHSK1Question.objects.create(
                    correct_letter=correct_letter,
                    task=task4
                )
                
                for letter in ['A', 'B', 'C']:
                    option_text = request.POST.get(f'task4_option{letter}_{i}')
                    FourthTaskHSK1Option.objects.create(
                        letter=letter,
                        text=option_text,
                        question=question
                    )
            
            return redirect('hsk1:listening_detail', pk=listening_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class ListeningDetailView(DetailView):
    model = ListeningHSK1
    template_name = 'hsk1/listening_detail.html'
    context_object_name = 'listening'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listening = self.object
        
        context['task1'] = listening.first_type_tasks.first()
        context['task2'] = listening.second_type_tasks.first()
        context['task3'] = listening.third_type_tasks.first()
        context['task4'] = listening.fourth_type_tasks.first()
        
        return context


class ListeningUpdateView(UpdateView):
    model = ListeningHSK1
    template_name = 'hsk1/create_listening.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        listening = self.object
        context['listening'] = listening
        context['is_update'] = True
        
        task1 = listening.first_type_tasks.first()
        if task1:
            context['task1_picture_id'] = task1.picture_id
            context['task1_questions'] = list(task1.questions.all())
        
        task2 = listening.second_type_tasks.first()
        if task2:
            context['task2_picture_id'] = task2.picture_id
            context['task2_questions'] = list(task2.questions.all())
        
        task3 = listening.third_type_tasks.first()
        if task3:
            context['task3_picture_id'] = task3.picture_id
            context['task3_questions'] = list(task3.questions.all())
        
        task4 = listening.fourth_type_tasks.first()
        if task4:
            task4_questions = list(task4.questions.all())
            context['task4_questions'] = task4_questions

            task4_options = {}
            for question in task4_questions:
                task4_options[question.id] = {opt.letter: opt.text for opt in question.options.all()}
            context['task4_options'] = task4_options
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        listening = self.object
        
        try:

            audio_id = request.POST.get('audio_id')
            listening.audio_id = audio_id
            listening.save()
            
            task1 = listening.first_type_tasks.first()
            if task1:
                task1.picture_id = request.POST.get('task1_picture_id')
                task1.save()

                questions = list(task1.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].is_correct = request.POST.get(f'task1_question_{i}') == 'true'
                        questions[i-1].save()
            

            task2 = listening.second_type_tasks.first()
            if task2:
                task2.picture_id = request.POST.get('task2_picture_id')
                task2.save()

                questions = list(task2.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].correct_letter = request.POST.get(f'task2_question_{i}')
                        questions[i-1].save()
            
            task3 = listening.third_type_tasks.first()
            if task3:
                task3.picture_id = request.POST.get('task3_picture_id')
                task3.save()

                questions = list(task3.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].correct_letter = request.POST.get(f'task3_question_{i}')
                        questions[i-1].save()
            
            
            task4 = listening.fourth_type_tasks.first()
            if task4:
                
                questions = list(task4.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        question = questions[i-1]
                        question.correct_letter = request.POST.get(f'task4_question_{i}')
                        question.save()
                        
                        
                        for letter in ['A', 'B', 'C']:
                            option_text = request.POST.get(f'task4_option{letter}_{i}')
                            
                            option = question.options.filter(letter=letter).first()
                            if option:
                                option.text = option_text
                                option.save()
            
            return redirect('hsk1:listening_detail', pk=listening.pk)
            
        except Exception as e:
            
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy('hsk1:listening_detail', kwargs={'pk': self.object.pk})


class ListeningDeleteView(DeleteView):
    model = ListeningHSK1
    template_name = 'hsk1/listening_confirm_delete.html'
    success_url = reverse_lazy('hsk1:listening_list')


### ЧТЕНИЕ

class ReadingListView(ListView):
    model = ReadingHSK1
    template_name = 'hsk1/reading_list.html'
    context_object_name = 'reading_variants'

class ReadingDetailView(DetailView):
    model = ReadingHSK1
    template_name = 'hsk1/reading_detail.html'
    context_object_name = 'reading'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reading = self.object
        
        # Получаем все связанные данные для отображения
        context['task1'] = reading.first_type_tasks.first()
        context['task2'] = reading.second_type_tasks.first()
        context['task3'] = reading.third_type_tasks.first()
        context['task4'] = reading.fourth_type_tasks.first()
        
        return context

class ReadingCreateView(CreateView):
    model = ReadingHSK1
    template_name = 'hsk1/reading_form.html'
    fields = []  # не используем стандартную форму
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант чтения
            reading_var = ReadingHSK1.objects.create()
            
            # 2. Задание 1
            task1_picture = request.POST.get('task1_picture_id')
            task1 = ReadingFirstTaskHSK1.objects.create(
                picture_id=task1_picture,
                reading_var=reading_var
            )
            # Варианты задания 1 (5 boolean вопросов)
            for i in range(1, 6):
                is_correct = request.POST.get(f'task1_question_{i}') == 'true'
                ReadingFirstTaskHSK1Option.objects.create(
                    is_correct=is_correct,
                    task=task1
                )
            
            # 3. Задание 2
            task2_picture = request.POST.get('task2_picture_id')
            task2 = ReadingSecondTaskHSK1.objects.create(
                picture_id=task2_picture,
                reading_var=reading_var
            )
            # Предложения задания 2
            for i in range(1, 6):
                text = request.POST.get(f'task2_text_{i}')
                correct_letter = request.POST.get(f'task2_question_{i}')
                ReadingSecondTaskHSK1Sentence.objects.create(
                    text=text,
                    correct_letter=correct_letter,
                    task=task2
                )
            
            # 4. Задание 3
            task3 = ReadingThirdTaskHSK1.objects.create(reading_var=reading_var)
            
            # Опции задания 3 (6 опций A-F)
            for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                option_text = request.POST.get(f'task3_option_{letter}')
                ReadingThirdTaskHSK1Option.objects.create(
                    letter=letter,
                    text=option_text,
                    task=task3
                )
            
            # Предложения задания 3 (5 вопросов)
            for i in range(1, 6):
                text = request.POST.get(f'task3_text_{i}')
                correct_letter = request.POST.get(f'task3_question_{i}')
                ReadingThirdTaskHSK1Sentence.objects.create(
                    text=text,
                    correct_letter=correct_letter,
                    task=task3
                )
            
            # 5. Задание 4
            task4 = ReadingFourthTaskHSK1.objects.create(reading_var=reading_var)
            
            # Опции задания 4 (6 опций A-F)
            for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                option_text = request.POST.get(f'task4_option_{letter}')
                ReadingFourthTaskHSK1Option.objects.create(
                    letter=letter,
                    text=option_text,
                    task=task4
                )
            
            # Предложения задания 4 (5 вопросов)
            for i in range(1, 6):
                text = request.POST.get(f'task4_text_{i}')
                correct_letter = request.POST.get(f'task4_question_{i}')
                ReadingFourthTaskHSK1Sentence.objects.create(
                    text=text,
                    correct_letter=correct_letter,
                    task=task4
                )
            
            return redirect('hsk1:reading_detail', pk=reading_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class ReadingUpdateView(UpdateView):
    model = ReadingHSK1
    template_name = 'hsk1/reading_form.html'
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
            context['task1_options'] = list(task1.options.all())
        
        # Задание 2
        task2 = reading.second_type_tasks.first()
        if task2:
            context['task2_picture_id'] = task2.picture_id
            context['task2_sentences'] = list(task2.sentences.all())
        
        # Задание 3
        task3 = reading.third_type_tasks.first()
        if task3:
            context['task3_options'] = {opt.letter: opt.text for opt in task3.options.all()}
            context['task3_sentences'] = list(task3.sentences.all())
        
        # Задание 4
        task4 = reading.fourth_type_tasks.first()
        if task4:
            context['task4_options'] = {opt.letter: opt.text for opt in task4.options.all()}
            context['task4_sentences'] = list(task4.sentences.all())
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        reading = self.object
        
        try:
            # Обновляем все задания аналогично CreateView
            # (код аналогичный CreateView, но с обновлением существующих объектов)
            
            # 1. Задание 1
            task1 = reading.first_type_tasks.first()
            if task1:
                task1.picture_id = request.POST.get('task1_picture_id')
                task1.save()
                options = list(task1.options.all())
                for i in range(1, 6):
                    if i <= len(options):
                        options[i-1].is_correct = request.POST.get(f'task1_question_{i}') == 'true'
                        options[i-1].save()
            
            # 2. Задание 2
            task2 = reading.second_type_tasks.first()
            if task2:
                task2.picture_id = request.POST.get('task2_picture_id')
                task2.save()
                sentences = list(task2.sentences.all())
                for i in range(1, 6):
                    if i <= len(sentences):
                        sentences[i-1].text = request.POST.get(f'task2_text_{i}')
                        sentences[i-1].correct_letter = request.POST.get(f'task2_question_{i}')
                        sentences[i-1].save()
            
            # 3. Задание 3
            task3 = reading.third_type_tasks.first()
            if task3:
                # Обновляем опции
                for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                    option_text = request.POST.get(f'task3_option_{letter}')
                    option = task3.options.filter(letter=letter).first()
                    if option:
                        option.text = option_text
                        option.save()
                
                # Обновляем предложения
                sentences = list(task3.sentences.all())
                for i in range(1, 6):
                    if i <= len(sentences):
                        sentences[i-1].text = request.POST.get(f'task3_text_{i}')
                        sentences[i-1].correct_letter = request.POST.get(f'task3_question_{i}')
                        sentences[i-1].save()
            
            # 4. Задание 4
            task4 = reading.fourth_type_tasks.first()
            if task4:
                # Обновляем опции
                for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                    option_text = request.POST.get(f'task4_option_{letter}')
                    option = task4.options.filter(letter=letter).first()
                    if option:
                        option.text = option_text
                        option.save()
                
                # Обновляем предложения
                sentences = list(task4.sentences.all())
                for i in range(1, 6):
                    if i <= len(sentences):
                        sentences[i-1].text = request.POST.get(f'task4_text_{i}')
                        sentences[i-1].correct_letter = request.POST.get(f'task4_question_{i}')
                        sentences[i-1].save()
            
            return redirect('hsk1:reading_detail', pk=reading.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy('hsk1:reading_detail', kwargs={'pk': self.object.pk})

class ReadingDeleteView(DeleteView):
    model = ReadingHSK1
    template_name = 'hsk1/reading_confirm_delete.html'
    success_url = reverse_lazy('hsk1:reading_list')