# Generated by Django 5.2.4 on 2025-07-21 10:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enciclopedia', '0005_enciclopediaattacchi_utente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enciclopediaattacchi',
            name='contromisure',
        ),
        migrations.RemoveField(
            model_name='enciclopediaattacchi',
            name='descrizione',
        ),
        migrations.RemoveField(
            model_name='enciclopediaattacchi',
            name='livello_rischio',
        ),
        migrations.RemoveField(
            model_name='enciclopediaattacchi',
            name='nome_attacco',
        ),
        migrations.RemoveField(
            model_name='enciclopediaattacchi',
            name='utente',
        ),
        migrations.CreateModel(
            name='Attacco',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome_attacco', models.CharField(max_length=255)),
                ('descrizione', models.TextField()),
                ('livello_rischio', models.CharField(choices=[('basso', 'Basso'), ('medio', 'Medio'), ('alto', 'Alto')], default='basso', max_length=100)),
                ('contromisure', models.TextField()),
                ('enciclopediaattacchi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enciclopedia.enciclopediaattacchi')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultazioneAttacco',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data_consultazione', models.DateTimeField(auto_now_add=True)),
                ('ora_consultazione', models.TimeField()),
                ('attacco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enciclopedia.attacco')),
                ('utente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enciclopedia.utente')),
            ],
        ),
    ]
