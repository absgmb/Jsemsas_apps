import simple_history.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="IncidentCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("code", models.CharField(max_length=40, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
    ]
