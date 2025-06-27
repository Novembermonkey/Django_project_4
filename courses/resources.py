from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Course, Subject


class CourseResource(resources.ModelResource):
    category = fields.Field(
        column_name='subject',
        attribute='subject',
        widget=ForeignKeyWidget(Subject, 'id'),
    )

    class Meta:
        model = Course
        fields = ('title', 'overview', 'duration', 'price', 'owner', 'subject', 'image', 'created')