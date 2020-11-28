# Generated by Django 3.0.5 on 2020-05-04 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("covid19", "0007_statespreadsheet_peer_review"),
    ]

    operations = [
        migrations.AlterField(
            model_name="statespreadsheet",
            name="boletim_notes",
            field=models.CharField(
                blank=True,
                default="",
                help_text='Observações no boletim como "depois de publicar o boletim a secretaria postou no Twitter que teve mais uma morte".',
                max_length=2000,
            ),
        ),
    ]
