from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import *

def get_sections(request):
    return render(request, "hsk3/sections.html")


class ListeningListView(ListView):
    model = Listening
    template_name = 'hsk3/listening_list.html'
    context_object_name = 'listening_variants'

class ListeningCreateView(CreateView):
    model = Listening
    template_name = 'hsk3/listening_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Создаем основной вариант
            audio_id = request.POST.get('audio_id')
            listening_var = Listening.objects.create(audio_id=audio_id)
            
            # 2. Задание 1 (5 вопросов A-F)
            task1_picture = request.POST.get('task1_picture_id')
            task1 = FirstTask.objects.create(
                picture_id=task1_picture,
                listening_var=listening_var
            )
            for i in range(1, 6):
                correct_letter = request.POST.get(f'task1_question_{i}')
                FirstTaskQuestion.objects.create(
                    correct_letter=correct_letter,
                    task=task1
                )
            
            # 3. Задание 2 (5 вопросов A-E) - используем FirstTask
            task2_picture = request.POST.get('task2_picture_id')
            task2 = FirstTask.objects.create(
                picture_id=task2_picture,
                listening_var=listening_var
            )
            for i in range(1, 6):
                correct_letter = request.POST.get(f'task2_question_{i}')
                FirstTaskQuestion.objects.create(
                    correct_letter=correct_letter,
                    task=task2
                )
            
            # 4. Задание 3 (10 boolean вопросов)
            for i in range(1, 11):
                text = request.POST.get(f'task3_text_{i}')
                is_correct = request.POST.get(f'task3_question_{i}') == 'true'
                SecondTask.objects.create(
                    text=text,
                    is_correct=is_correct,
                    listening_var=listening_var
                )
            
            # 5. Задание 4 (10 вопросов с вариантами A-C)
            task4 = ThirdTask.objects.create(listening_var=listening_var)
            for i in range(1, 11):
                correct_letter = request.POST.get(f'task4_question_{i}')
                question = ThirdTaskQuestion.objects.create(
                    correct_letter=correct_letter,
                    task=task4
                )
                # Варианты ответов
                for letter in ['A', 'B', 'C']:
                    option_text = request.POST.get(f'task4_option{letter}_{i}')
                    ThirdTaskOption.objects.create(
                        letter=letter,
                        text=option_text,
                        question=question
                    )
            
            # 6. Задание 5 (10 вопросов с вариантами A-C) - используем ThirdTask
            task5 = ThirdTask.objects.create(listening_var=listening_var)
            for i in range(1, 11):
                correct_letter = request.POST.get(f'task5_question_{i}')
                question = ThirdTaskQuestion.objects.create(
                    correct_letter=correct_letter,
                    task=task5
                )
                # Варианты ответов
                for letter in ['A', 'B', 'C']:
                    option_text = request.POST.get(f'task5_option{letter}_{i}')
                    ThirdTaskOption.objects.create(
                        letter=letter,
                        text=option_text,
                        question=question
                    )
            
            return redirect('hsk3:listening_detail', pk=listening_var.pk)
            
        except Exception as e:
            return self.render_to_response({
                'error': f'Ошибка при создании: {str(e)}'
            })

class ListeningDetailView(DetailView):
    model = Listening
    template_name = 'hsk3/listening_detail.html'
    context_object_name = 'listening'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listening = self.object
        
        # Получаем все задания для отображения
        first_tasks = list(listening.first_type_tasks.all())
        if len(first_tasks) > 0:
            context['task1'] = first_tasks[0]  # Первое задание первого типа
        if len(first_tasks) > 1:
            context['task2'] = first_tasks[1]  # Второе задание первого типа
        
        # Задание 3 - все объекты SecondTask
        context['task3_list'] = listening.second_type_tasks.all()
        
        # Для заданий 4 и 5 используем ThirdTask
        third_tasks = list(listening.third_type_tasks.all())
        if len(third_tasks) > 0:
            context['task4'] = third_tasks[0]  # Первое задание третьего типа
        if len(third_tasks) > 1:
            context['task5'] = third_tasks[1]  # Второе задание третьего типа
        
        return context

class ListeningUpdateView(UpdateView):
    model = Listening
    template_name = 'hsk3/listening_form.html'
    fields = []
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        listening = self.object
        context['listening'] = listening
        context['is_update'] = True
        
        # Задания 1 и 2 (FirstTask)
        first_tasks = list(listening.first_type_tasks.all())
        if len(first_tasks) > 0:
            task1 = first_tasks[0]
            context['task1_picture_id'] = task1.picture_id
            context['task1_questions'] = list(task1.questions.all())
        
        if len(first_tasks) > 1:
            task2 = first_tasks[1]
            context['task2_picture_id'] = task2.picture_id
            context['task2_questions'] = list(task2.questions.all())
        
        # Задание 3 (SecondTask)
        task3_list = list(listening.second_type_tasks.all())
        context['task3_list'] = task3_list
        
        # Задания 4 и 5 (ThirdTask)
        third_tasks = list(listening.third_type_tasks.all())
        if len(third_tasks) > 0:
            task4 = third_tasks[0]
            task4_questions = list(task4.questions.all())
            context['task4_questions'] = task4_questions
            # Собираем варианты ответов для задания 4
            task4_options = {}
            for question in task4_questions:
                task4_options[question.id] = {opt.letter: opt.text for opt in question.options.all()}
            context['task4_options'] = task4_options
        
        if len(third_tasks) > 1:
            task5 = third_tasks[1]
            task5_questions = list(task5.questions.all())
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
            first_tasks = list(listening.first_type_tasks.all())
            if len(first_tasks) > 0:
                task1 = first_tasks[0]
                task1.picture_id = request.POST.get('task1_picture_id')
                task1.save()
                # Обновляем вопросы задания 1
                questions = list(task1.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].correct_letter = request.POST.get(f'task1_question_{i}')
                        questions[i-1].save()
            
            # 3. Обновляем Задание 2
            if len(first_tasks) > 1:
                task2 = first_tasks[1]
                task2.picture_id = request.POST.get('task2_picture_id')
                task2.save()
                # Обновляем вопросы задания 2
                questions = list(task2.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].correct_letter = request.POST.get(f'task2_question_{i}')
                        questions[i-1].save()
            
            # 4. Обновляем Задание 3
            task3_list = list(listening.second_type_tasks.all())
            for i in range(1, 11):
                if i <= len(task3_list):
                    task3 = task3_list[i-1]
                    task3.text = request.POST.get(f'task3_text_{i}')
                    task3.is_correct = request.POST.get(f'task3_question_{i}') == 'true'
                    task3.save()
            
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
                for i in range(1, 11):
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
            
            return redirect('hsk3:listening_detail', pk=listening.pk)
            
        except Exception as e:
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy('hsk3:listening_detail', kwargs={'pk': self.object.pk})

class ListeningDeleteView(DeleteView):
    model = Listening
    template_name = 'hsk3/listening_confirm_delete.html'
    success_url = reverse_lazy('hsk3:listening_list')