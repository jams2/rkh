# Generated by Django 3.1 on 2020-08-30 10:28

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0052_pagelogentry'),
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='FancyPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.core.fields.StreamField([('main_content', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('sub_section', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('content', wagtail.core.blocks.RichTextBlock()), ('link_1', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_url', wagtail.core.blocks.URLBlock(required=False))], required=True)), ('link_2', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock()), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_url', wagtail.core.blocks.URLBlock(required=False))], required=True))])), ('image_gallery', wagtail.core.blocks.StreamBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.CharBlock(required=False))], max_num=16))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
