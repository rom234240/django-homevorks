from django.db import migrations, models

def transfer_data(apps, schema_editor):
    Student = apps.get_model('school', 'Student')
    Teacher = apps.get_model('school', 'Teacher')
    for student in Student.objects.all():
        if student.teacher_id:
            teacher = Teacher.objects.get(pk=student.teacher_id)
            student.teachers.add(teacher)

class Migration(migrations.Migration):
    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='teachers',
            field=models.ManyToManyField(
                related_name='students',
                to='school.Teacher',
                blank=True
            ),
        ),
        migrations.RunPython(transfer_data),
        migrations.RemoveField(
            model_name='student',
            name='teacher',
        ),
    ]