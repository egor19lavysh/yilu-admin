from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import ListeningHSK1
from .forms import ListeningVariantForm
from hsk1.models import *


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
    template_name = 'hsk1/create_listening.html'  # тот же шаблон что и для создания
    fields = []  # не используем стандартную форму
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        # Заполняем контекст существующими данными для предзаполнения формы
        listening = self.object
        context['listening'] = listening
        context['is_update'] = True  # флаг что это редактирование
        
        # Задание 1
        task1 = listening.first_type_tasks.first()
        if task1:
            context['task1_picture_id'] = task1.picture_id
            context['task1_questions'] = list(task1.questions.all())
        
        # Задание 2
        task2 = listening.second_type_tasks.first()
        if task2:
            context['task2_picture_id'] = task2.picture_id
            context['task2_questions'] = list(task2.questions.all())
        
        # Задание 3
        task3 = listening.third_type_tasks.first()
        if task3:
            context['task3_picture_id'] = task3.picture_id
            context['task3_questions'] = list(task3.questions.all())
        
        # Задание 4
        task4 = listening.fourth_type_tasks.first()
        if task4:
            task4_questions = list(task4.questions.all())
            context['task4_questions'] = task4_questions
            # Собираем варианты ответов для каждого вопроса
            task4_options = {}
            for question in task4_questions:
                task4_options[question.id] = {opt.letter: opt.text for opt in question.options.all()}
            context['task4_options'] = task4_options
        
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
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].is_correct = request.POST.get(f'task1_question_{i}') == 'true'
                        questions[i-1].save()
            
            # 3. Обновляем Задание 2
            task2 = listening.second_type_tasks.first()
            if task2:
                task2.picture_id = request.POST.get('task2_picture_id')
                task2.save()
                # Обновляем вопросы задания 2
                questions = list(task2.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].correct_letter = request.POST.get(f'task2_question_{i}')
                        questions[i-1].save()
            
            # 4. Обновляем Задание 3
            task3 = listening.third_type_tasks.first()
            if task3:
                task3.picture_id = request.POST.get('task3_picture_id')
                task3.save()
                # Обновляем вопросы задания 3
                questions = list(task3.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        questions[i-1].correct_letter = request.POST.get(f'task3_question_{i}')
                        questions[i-1].save()
            
            # 5. Обновляем Задание 4
            task4 = listening.fourth_type_tasks.first()
            if task4:
                # Обновляем вопросы и варианты задания 4
                questions = list(task4.questions.all())
                for i in range(1, 6):
                    if i <= len(questions):
                        question = questions[i-1]
                        question.correct_letter = request.POST.get(f'task4_question_{i}')
                        question.save()
                        
                        # Обновляем варианты ответов для вопроса
                        for letter in ['A', 'B', 'C']:
                            option_text = request.POST.get(f'task4_option{letter}_{i}')
                            # Находим существующий вариант
                            option = question.options.filter(letter=letter).first()
                            if option:
                                option.text = option_text
                                option.save()
            
            return redirect('hsk1:listening_detail', pk=listening.pk)
            
        except Exception as e:
            # Обработка ошибок
            context = self.get_context_data()
            context['error'] = f'Ошибка при обновлении: {str(e)}'
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy('hsk1:listening_detail', kwargs={'pk': self.object.pk})

# Удаление варианта
class ListeningDeleteView(DeleteView):
    model = ListeningHSK1
    template_name = 'hsk1/listening_confirm_delete.html'
    success_url = reverse_lazy('hsk1:listening_list')