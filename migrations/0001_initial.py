# Generated by Django 5.1.7 on 2025-03-25 09:17

import datetime
import django.db.models.deletion
import django.utils.timezone
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.contrib.forms.models
import wagtail.fields
import wagtailmarkdown.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('wagtailcore', '0094_alter_page_locale'),
        ('wagtaildocs', '0014_alter_document_file_size'),
        ('wagtailimages', '0027_image_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('show_pagetitle', models.BooleanField(default=True, help_text='If the page title should be shown')),
                ('order_by', models.CharField(blank=True, choices=[('-order_by_date', 'Orderby Date >'), ('order_by_date', 'Orderby Date <'), ('-latest_revision_created_at', 'Update Date/Time >'), ('latest_revision_created_at', 'Update Date/Time <'), ('-first_published_at', 'Publish Date/Time >'), ('first_published_at', 'Publish Date/Time <'), ('title', 'Title'), ('-title', 'Title >')], default=('-order_by_date', 'Orderby Date >'), help_text='The article attribute to determine the order in which articles will be displayed', max_length=40)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BaseArticlePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body_md', wagtailmarkdown.fields.MarkdownField(blank=True, help_text='A markdown version of the body. Both this and the streamfield version body will be displayed if they have content')),
                ('body_sf', wagtail.fields.StreamField([('paragraph_block', 0), ('heading_block', 3), ('document_block', 4), ('quote_block', 5), ('image_block', 10), ('external_image_block', 12), ('embed_block', 13), ('table', 14)], blank=True, block_lookup={0: ('wagtail.blocks.RichTextBlock', (), {'features': ['link', 'bold', 'italic', 'ol', 'ul'], 'icon': 'pilcrow'}), 1: ('wagtail.blocks.CharBlock', (), {'form_classname': 'title', 'required': True}), 2: ('wagtail.blocks.ChoiceBlock', [], {'blank': True, 'choices': [('', 'Select a heading size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')], 'required': False}), 3: ('wagtail.blocks.StructBlock', [[('heading_text', 1), ('size', 2)]], {}), 4: ('wagtail.documents.blocks.DocumentChooserBlock', (), {}), 5: ('wagtail.blocks.BlockQuoteBlock', (), {}), 6: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': True}), 7: ('wagtail.blocks.CharBlock', (), {'required': False}), 8: ('wagtail.blocks.CharBlock', (), {'required': True}), 9: ('wagtail.blocks.URLBlock', (), {'required': False}), 10: ('wagtail.blocks.StructBlock', [[('image', 6), ('caption', 7), ('attribution', 7), ('alt', 8), ('link', 9)]], {}), 11: ('wagtail.blocks.URLBlock', (), {'required': True}), 12: ('wagtail.blocks.StructBlock', [[('url', 11), ('caption', 7), ('attribution', 7), ('alt', 8), ('link', 9)]], {}), 13: ('wagtail.embeds.blocks.EmbedBlock', (), {'help_text': 'Insert a URL to embed. For example, https://www.youtube.com/watch?v=SGJFWirQ3ks', 'icon': 'media'}), 14: ('wagtail.contrib.table_block.blocks.TableBlock', (), {})}, help_text='A streamfield version of the body. Both this and the markdown version body will be displayed if they have content')),
                ('embed_url', models.URLField(blank=True, help_text='For pages with an iFrame, the URL of the embedded contnet', max_length=765, verbose_name='Embed Target URL')),
                ('embed_frame_style', models.CharField(blank=True, default='width:90%; height:1600px;', help_text='For pages with an iFrame, styling for the frame', max_length=255, verbose_name='Frame Style')),
                ('show_doc_link', models.BooleanField(default=True, help_text="Show the document link automatically.  One reason to set false would be you're already placing a link in the body", verbose_name='show doc link')),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.document')),
            ],
            options={
                'verbose_name': 'Base Article',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticleStaticTagsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('show_pagetitle', models.BooleanField(default=True, help_text='If the page title should be shown')),
                ('included_tag_names_string', models.CharField(blank=True, help_text='A comma separated list of tags to be included in this page which can also be grouped - separate groups with semicolon', max_length=255, verbose_name='tags included')),
                ('tag_titles_string', models.CharField(blank=True, help_text='A comma separated list of titles to be used instead of the tag names - not separated by group', max_length=255, verbose_name='tag titles')),
                ('group_titles_string', models.CharField(blank=True, help_text='A comma separated list of titles to be used for tag groups', max_length=255, verbose_name='group titles')),
                ('apply_special_formatting', models.IntegerField(default=0, help_text='The group number up to which special formatting should be applied.  Implementation may vary by template app', verbose_name='apply special formatting')),
                ('show_body_in_index', models.IntegerField(default=0, help_text='The group number up to which articles will show the entire body instead of the summary', verbose_name='show body instead of summary')),
                ('separate_tag_groups', models.BooleanField(default=True, help_text='If the ArticlePages should be separated by tag')),
                ('show_tag_titles', models.BooleanField(default=True, help_text='If the tag name should be displayed as a title to accompany the ArticlePages')),
                ('order_by', models.CharField(choices=[('-order_by_date', 'Orderby Date >'), ('order_by_date', 'Orderby Date <'), ('-latest_revision_created_at', 'Update Date/Time >'), ('latest_revision_created_at', 'Update Date/Time <'), ('-first_published_at', 'Publish Date/Time >'), ('first_published_at', 'Publish Date/Time <'), ('title', 'Title'), ('-title', 'Title >')], default=('-order_by_date', 'Orderby Date >'), help_text='The article attribute to determine the order in which articles will be displayed', max_length=40)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('to_address', models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, validators=[wagtail.contrib.forms.models.validate_to_address], verbose_name='to address')),
                ('from_address', models.EmailField(blank=True, max_length=255, verbose_name='from address')),
                ('subject', models.CharField(blank=True, max_length=255, verbose_name='subject')),
                ('intro', wagtail.fields.RichTextField(blank=True, help_text="Enter something like a summary of the form's purpose or general instructions for filling it out. If your form contains honeypots, explain that the form has fields or a field which should be left blank")),
                ('thank_you_text', wagtail.fields.RichTextField(blank=True, help_text='Enter text to be shown after the form is submitted')),
                ('honeypot_field_names', models.CharField(blank=True, help_text='The name or comma-separated list of names for the field or fields to be left blank by humans in order to trap bots. The field(s) should be single-line required=False', max_length=255, verbose_name='honeypot')),
                ('honeypot_error_message', models.CharField(blank=True, default='If you are a person, please read the notes and retry', help_text='The name or comma-separated list of names for the field or fields to be left blank by humans in order to trap bots. The field(s) should be single-line required=False', max_length=255, verbose_name='honeypot error message')),
                ('honeypot_intro', wagtail.fields.RichTextField(blank=True, default='Note: This form has a field or fields which should be left unfilled. In order to trap automatic form fillers, these fields are not marked but a person should be able to figure out which those are', help_text='Explain to visitors that the form has a field or fields which humans should realize are to be left blank')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.forms.models.FormMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='SidebarPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('show_pagetitle', models.BooleanField(default=True, help_text='If the page title should be shown')),
                ('location', models.CharField(blank=True, choices=[('left', 'left'), ('right', 'right'), ('top', 'top'), ('bottom', 'bottom')], max_length=40, verbose_name='location')),
                ('order_by', models.CharField(blank=True, choices=[('-order_by_date', 'Orderby Date >'), ('order_by_date', 'Orderby Date <'), ('title', 'Title'), ('-title', 'Title >')], default=('-order_by_date', 'Orderby Date >'), help_text='The article attribute to determine the order in which articles will be displayed', max_length=40)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticleCommentPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Post date')),
                ('body', models.CharField(blank=True, help_text='The body of the comment', max_length=250)),
                ('commenter_display_name', models.CharField(blank=True, help_text='The body of the comment', max_length=250)),
                ('in_reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='webikwa.articlecommentpage')),
            ],
            options={
                'verbose_name': 'Comment',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('basearticlepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='webikwa.basearticlepage')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Post date')),
                ('order_by_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='A date optionally used for ordering. Can be used instead of post date in order to avoid changing the post date')),
                ('summary', models.CharField(blank=True, help_text='A summary to be displayed instead of the body for index views', max_length=250)),
                ('show_gallery', models.BooleanField(default=True, help_text='Show the gallery', verbose_name='show gallery')),
            ],
            options={
                'verbose_name': 'Article',
            },
            bases=('webikwa.basearticlepage',),
        ),
        migrations.CreateModel(
            name='FreeArticlePage',
            fields=[
                ('basearticlepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='webikwa.basearticlepage')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Post date')),
                ('order_by_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='A date optionally used for ordering. Can be used instead of post date in order to avoid changing the post date')),
                ('show_gallery', models.BooleanField(default=True, help_text='Show the gallery', verbose_name='show gallery')),
            ],
            options={
                'verbose_name': 'Free Article',
            },
            bases=('webikwa.basearticlepage',),
        ),
        migrations.CreateModel(
            name='SidebarArticlePage',
            fields=[
                ('basearticlepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='webikwa.basearticlepage')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Post date')),
                ('order_by_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='A date optionally used for ordering. Can be used instead of post date in order to avoid changing the post date')),
            ],
            options={
                'abstract': False,
            },
            bases=('webikwa.basearticlepage',),
        ),
        migrations.CreateModel(
            name='ArticlePageGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('alt_text', models.TextField(blank=True, max_length=250, verbose_name='alt text')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='webikwa.basearticlepage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticlePageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('alt_text', models.TextField(blank=True, max_length=250, verbose_name='alt text')),
                ('display_with_summary', models.BooleanField(default=False, help_text='If this image should appear where the article summary is shown', verbose_name='with summary')),
                ('display_before_body', models.BooleanField(default=False, help_text='If this image should appear before the body of the article', verbose_name='before body')),
                ('display_after_body', models.BooleanField(default=False, help_text='If this image should appear after the body of the article', verbose_name='after_body')),
                ('is_featured', models.IntegerField(choices=[(0, 'Never'), (1, 'If First')], default=1, help_text='If this image is the featured image to be used in social media links and similar contexts', verbose_name='is featured')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_images', to='webikwa.basearticlepage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('author_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('clean_name', models.CharField(blank=True, default='', help_text='Safe name of the form field, the label converted to ascii_snake_case', max_length=255, verbose_name='name')),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label')),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time'), ('hidden', 'Hidden field')], max_length=16, verbose_name='field type')),
                ('required', models.BooleanField(default=True, verbose_name='required')),
                ('choices', models.TextField(blank=True, help_text='Comma or new line separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices')),
                ('default_value', models.TextField(blank=True, help_text='Default value. Comma or new line separated values supported for checkboxes.', verbose_name='default value')),
                ('help_text', models.CharField(blank=True, max_length=255, verbose_name='help text')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='webikwa.formpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RedirectPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('target_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='SiteSpecificImportantPages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_index_page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiteTemplateSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_style', models.CharField(blank=True, default='50%', help_text='Inline styling for the header', max_length=255)),
                ('show_banner_image', models.BooleanField(default=True, help_text='Show the chosen banner image.  If deselected, banner_text will be used instead of the image', verbose_name='show banner image')),
                ('banner_image_style', models.CharField(blank=True, default='50%', help_text='Styling for the banner image or if a single value, A css value representing the width of the banner image. Include at least one semicolon (;) to indicate that this is a style, and not just a width value', max_length=255)),
                ('banner_text', models.CharField(blank=True, default='webikwa', help_text='The alt text to be displayed if there is a banner image, or the text to be displayed if there is no image', max_length=80, verbose_name='banner_text')),
                ('site_description', models.CharField(blank=True, default='New Wibewa Wagtail Blog', help_text='The site description to be displayed near the banner image or banner text', max_length=80, verbose_name='site description')),
                ('show_leftbar', models.BooleanField(default=False, help_text='If the left sidebar should be shown - requires a template named wibewa/includes/sidebarleft.html')),
                ('show_rightbar', models.BooleanField(default=False, help_text='If the right sidebar should be shown - requires a template named wibewa/includes/sidebarright.html')),
                ('mainmenu_location', models.CharField(choices=[('none', 'None'), ('top', 'Top'), ('left', 'Left'), ('right', 'Right')], default='top', help_text='The location of the main menu', max_length=20, verbose_name='main menu location')),
                ('theme_color', models.CharField(default='black', help_text='The theme color. This should match the base name of a css file in a static folder webikwa/css. Ex "blue" if there is a webikwa/css/blue.css', max_length=30, verbose_name='theme color')),
                ('footer_text', models.CharField(blank=True, default='Created wth Wagtail and webikwa', help_text='The footer text.  This may be split into a list using footer_text_separator', max_length=255, verbose_name='footer text')),
                ('footer_text_separator', models.CharField(blank=True, default=';', help_text='The character by which the footer text will be split into a list.  This is optional', max_length=2, verbose_name='footer text separator')),
                ('favicon', models.CharField(blank=True, help_text="The path to the favicon. If static, precede with 'static:' ex: static:images/favicon.ico", max_length=125, verbose_name='path to favicon')),
                ('banner_image', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.site')),
            ],
            options={
                'verbose_name_plural': 'Template Settings',
            },
        ),
        migrations.CreateModel(
            name='ArticlePageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='webikwa.articlepage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='articlepage',
            name='authors',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='webikwa.author'),
        ),
        migrations.AddField(
            model_name='articlepage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='webikwa.ArticlePageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
