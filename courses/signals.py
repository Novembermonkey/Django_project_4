from django.db.models.signals import pre_delete
from courses.models import Course
from .resources import CourseResource
from django.dispatch import receiver
import json

@receiver(pre_delete, sender=Course)
def course_pre_delete(sender, instance, **kwargs):
    resource = CourseResource()
    dataset = resource.export([instance])
    deleted_product = json.loads(dataset.json)[0]

    with open('courses/backups/deleted_courses.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    data.append(deleted_product)

    with open('courses/backups/deleted_courses.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)