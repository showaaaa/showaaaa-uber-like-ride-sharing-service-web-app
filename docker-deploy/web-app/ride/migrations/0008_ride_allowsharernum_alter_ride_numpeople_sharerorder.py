# Generated by Django 4.1.5 on 2023-02-04 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ride', '0007_alter_ride_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='allowSharernum',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='No sharer please choose 0'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='numPeople',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='SharerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destAddr', models.CharField(max_length=50)),
                ('numPeople', models.IntegerField(default=1)),
                ('earliestDate', models.DateTimeField(help_text='Format: 2023-01-01 12:00')),
                ('latestDate', models.DateTimeField(help_text='Format: 2023-01-01 12:00')),
                ('orderOwner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderOwner', to=settings.AUTH_USER_MODEL)),
                ('sharerride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sharerride', to='ride.ride')),
            ],
        ),
    ]