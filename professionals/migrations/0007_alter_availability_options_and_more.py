from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professionals', '0006_alter_professionals_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='day',
            field=models.IntegerField(
                choices=[
                    (0, 'Monday'),
                    (1, 'Tuesday'),
                    (2, 'Wednesday'),
                    (3, 'Thursday'),
                    (4, 'Friday'),
                    (5, 'Saturday'),
                    (6, 'Sunday'),
                ],
                default=0,
            ),
            preserve_default=False,
        ),

        migrations.AddField(
            model_name='availability',
            name='session_type',
            field=models.CharField(
                choices=[
                    ('morning', 'Morning'),
                    ('afternoon', 'Afternoon'),
                ],
                default='morning',
                max_length=10,
            ),
            preserve_default=False,
        ),

        migrations.RemoveField(
            model_name='availability',
            name='available_date',
        ),

        migrations.AlterModelOptions(
            name='availability',
            options={'ordering': ['day', 'start_time']},
        ),

        migrations.AlterUniqueTogether(
            name='availability',
            unique_together={
                ('professional', 'day', 'session_type')
            },
        ),
    ]