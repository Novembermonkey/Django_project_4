from django.urls import path
from courses import views

app_name = 'courses'

urlpatterns = [
            path('', views.Index.as_view(), name='index'),
            path('course-list/', views.CourseList.as_view(), name='course_list'),
            path('subject/<slug:subject_slug>', views.Index.as_view(), name='courses_by_subject'),
            path('course/detail/<int:pk>', views.CourseDetail.as_view(), name='course_detail'),
            path('course/detail/<int:pk>/comment/create', views.CommentCreate.as_view(), name='create_comment'),
            path('course/lesson/<int:pk>', views.LessonDetail.as_view(), name='lesson_detail'),
            path('course/teachers/', views.TeacherList.as_view(), name='teachers_list'),
            path('index2/', views.index2, name='index2'),
]