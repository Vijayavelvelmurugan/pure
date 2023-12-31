# Generated by Django 4.2.6 on 2023-10-29 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_userimages_image_alter_userimages_user_record'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fancy_dress_image', models.ImageField(upload_to='fancy_dress/')),
                ('drawing_image', models.ImageField(upload_to='drawing/')),
                ('essay_image', models.ImageField(upload_to='essay/')),
            ],
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='mobile_number',
            field=models.CharField(max_length=20),
        ),
    ]
