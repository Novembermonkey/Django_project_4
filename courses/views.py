from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from courses.models import Course, Subject, Comment, Lesson, Module
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from users.models import CustomUser


# Create your views here.

def index2(request):
    return render(request, 'courses/lesson_detail.html')


class Index(ListView):
    model = Course
    template_name = 'courses/index.html'
    context_object_name = 'courses'

    def get_queryset(self):
        courses = Course.objects.all()

        subject_slug = self.kwargs.get('subject_slug')
        if subject_slug:
            courses = courses.filter(subject__slug=subject_slug)

        return courses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = Subject.objects.all()
        subjects.annotate(course_count=Count('courses'))
        context['subjects'] = subjects

        subject_slug = self.kwargs.get('subject_slug')
        if subject_slug:
            context['subject'] = Subject.objects.get(slug=subject_slug)
            self.template_name = 'courses/course.html'
        print(context)
        return context


class CourseList(ListView):
    model = Course
    template_name = 'courses/course.html'
    context_object_name = 'courses'
    extra_context = {'subjects': Subject.objects.all()}


class CourseDetail(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    pk_url_kwarg = 'pk'


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'courses/course_detail.html'
    fields = ('topic', 'content', 'rating')
    login_url = 'users:login_page'

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context

    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        form.instance.course = course
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('courses:course_detail', kwargs={'pk': pk})


class LessonDetail(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    pk_url_kwarg = 'pk'
    login_url = 'users:login_page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=self.kwargs.get('pk'))
        course = lesson.module.course

        context['course'] = course
        context['modules'] = course.modules.all()
        context['current_lesson'] = lesson

        return context


class TeacherList(ListView):
    model = CustomUser
    template_name = 'courses/teacher.html'

    def get_queryset(self):
        teachers = CustomUser.objects.filter(role__name='teacher')
        return teachers