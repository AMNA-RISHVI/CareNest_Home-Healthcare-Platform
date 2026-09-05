from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_alter_appointment_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointment_fee_paid',
            field=models.BooleanField(default=False),
        ),
    ]