import datetime
import re
import sys
from django import forms
from django.db import models
from django.conf import settings
from django.utils import timezone
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,

)
from wagtail.contrib.forms.utils import get_field_clean_name
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.models import AbstractForm, AbstractEmailForm, AbstractFormField,FORM_FIELD_CHOICES
from wagtail.contrib.forms.panels import FormSubmissionsPanel

from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)

from wagtail.fields import StreamField, RichTextField
from wagtail.documents import get_document_model

from wagtail.models import Page, Orderable

from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtailmarkdown.fields import MarkdownField

from .blocks import BodyStreamBlock

def get_sidebars(request):
    sidebars = []
    for sidebarpage in SidebarPage.objects.live().all():
        sidebar = {"location":sidebarpage.location, "children":[]}
        for childpage in sidebarpage.get_children():
            child={"title":childpage.title, "body_md":childpage.specific.body_md, "body_sf":childpage.specific.body_sf, "context": childpage.specific.get_context(request)}
            sidebar["children"].append(child)
        sidebars.append(sidebar)
    return sidebars

class RedirectPage(Page):

    target_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        PageChooserPanel('target_page'),
    ]

    def route(self, request, path_components):
        if path_components:
            return super().route(request, path_components)
        else:
            path_components=[self.target_page.slug]
            return super().route(request, path_components)

class ArticleSingularPage(Page):

    target_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        PageChooserPanel('target_page', page_type=['webikwa.ArticlePage']),
    ]


class ArticleIndexPage(Page):
    intro = RichTextField(blank=True)
    show_pagetitle=models.BooleanField( default=True, help_text="If the page title should be shown" )

    order_by_choices=(
        ('-order_by_date','Orderby Date >'),
        ('order_by_date','Orderby Date <'),
        ('-latest_revision_created_at','Update Date/Time >'),
        ('latest_revision_created_at','Update Date/Time <'),
        ('-first_published_at','Publish Date/Time >'),
        ('first_published_at','Publish Date/Time <'),
        ('title','Title'),
        ('-title','Title >'),
    )

    order_by_field = models.CharField(max_length=40,blank=True, choices=order_by_choices, default=order_by_choices[0][0],help_text='The article attribute to determine the order in which articles will be displayed')

    subpage_types = ["ArticlePage"]

    content_panels = Page.content_panels + [
        FieldPanel('show_pagetitle'),
        FieldPanel('intro'),
        FieldPanel('order_by_field'),
    ]

    def get_context(self, request):

        tag = request.GET.get('tag')

        context = super().get_context(request)

#        ArticlePages = self.get_children().specific().live().order_by(self.order_by_field)
        ArticlePages = ArticlePage.objects.live().order_by(self.order_by_field)
        if tag:
            ArticlePages = ArticlePage.objects.filter(tags__name=tag)

        context['articlepages'] = ArticlePages

        context['sidebars'] = get_sidebars(request)

        return context

class SidebarPage(Page):
    intro = RichTextField(blank=True)
    show_pagetitle=models.BooleanField( default=True, help_text="If the page title should be shown" )
    location = models.CharField("location", max_length=40, blank=True, choices=(("left","left"),("right","right"),("top","top"),("bottom","bottom")))

    order_by_choices=(
        ('-order_by_date','Orderby Date >'),
        ('order_by_date','Orderby Date <'),
        ('title','Title'),
        ('-title','Title >'),
    )

    order_by_field = models.CharField(max_length=40,blank=True, choices=order_by_choices, default=order_by_choices[0], help_text='The article attribute to determine the order in which articles will be displayed')

    content_panels = Page.content_panels + [
        FieldPanel('show_pagetitle'),
        FieldPanel('intro'),
        FieldPanel('location'),
        FieldPanel('order_by_field')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        ArticlePages = self.get_children().live().order_by(self.order_by_field)
        context['articlepages'] = ArticlePages
        return context

@register_snippet
class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticlePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BaseArticlePage(Page):

    body_md = MarkdownField(blank=True, help_text="A markdown version of the body. Both this and the streamfield version body will be displayed if they have content")
    body_sf = StreamField(BodyStreamBlock(), blank=True, use_json_field=True, help_text="A streamfield version of the body. Both this and the markdown version body will be displayed if they have content")
    embed_url = models.URLField("Embed Target URL", max_length=765, blank=True, help_text="For pages with an iFrame, the URL of the embedded contnet")
    embed_frame_style = models.CharField("Frame Style", max_length=255, blank=True, default="width:90%; height:1600px;", help_text="For pages with an iFrame, styling for the frame")
    document = models.ForeignKey(get_document_model(), null=True,blank=True,on_delete=models.SET_NULL,)
    show_doc_link = models.BooleanField("show doc link", default=True, help_text="Show the document link automatically.  One reason to set false would be you're already placing a link in the body")

    is_creatable = False

    class Meta:
        verbose_name = "Base Article"

    def get_context(self, request):
        context=super().get_context(request)

        # restrict allowable embeds by listing them in settings.  "https://tougshire.com/12345" will match if "https://tougshire.com" is listed
        allow_embed = False
        if self.embed_url:
            if hasattr(settings,"ALLOWED_EMBED_URLS"):
                for allowed_url in settings.ALLOWED_EMBED_URLS:
                    if allowed_url in self.embed_url[0:len(allowed_url)]:
                        allow_embed = True
            else:
                allow_embed = True

            if allow_embed:
                context['embed_url'] = self.embed_url
                context['embed_frame_style'] = self.embed_frame_style

        return context

    def featured_image(self):
        try:
            return self.article_images.filter(is_featured=True).first()
        except ArticlePageImage.DoesNotExist:
            try:
                return self.article_images.first()
            except ArticlePageImage.DoesNotExist:
                return None


class ArticlePage(BaseArticlePage):

    date = models.DateField("Post date", default=datetime.date.today)
    order_by_date = models.DateTimeField(default=timezone.now, blank=True, help_text="A date optionally used for ordering. Can be used instead of post date in order to avoid changing the post date")
    summary = models.CharField(max_length=250, blank=True, help_text='A summary to be displayed instead of the body for index views')

    authors = ParentalManyToManyField('webikwa.Author', blank=True)
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)

    show_gallery = models.BooleanField("show gallery", default=True, help_text="Show the gallery")

    parent_page_types = ["ArticleIndexPage"]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('date'),
                FieldPanel('order_by_date'),
                FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
                FieldPanel('tags'),
            ],
            heading="Article information"
        ),
        FieldPanel('summary'),
        FieldPanel('body_md'),
        FieldPanel('body_sf'),
        MultiFieldPanel(
            [
                FieldPanel('document'),
                FieldPanel('show_doc_link'),
            ],
            heading="Document"
        ),
        MultiFieldPanel(
            [
                InlinePanel('article_images', label="Article images"),
                InlinePanel('gallery_images', label="Gallery images"),
                FieldPanel('show_gallery'),
            ]
        ),
        MultiFieldPanel(
            [
                FieldPanel('embed_url'),
                FieldPanel('embed_frame_style'),
            ],
            heading="Embedded Content"
        ),

    ]

    search_fields = Page.search_fields + [
        index.SearchField('summary'),
        index.SearchField('body_md'),
        index.SearchField('body_sf'),
    ]


    class Meta:
        verbose_name = "Article"

    def get_tags(self):
        tag_list=[ tag.name for tag in self.tags.all().order_by("name") ]
        return ",".join(tag_list)

    def get_context(self, request):
        context=super().get_context(request)

        context['sidebars'] = get_sidebars(request)

        context['visible_tags']=[]
        for tag in context['page'].tags.all():

            if not tag.name[0] == '_':
                context['visible_tags'].append(tag)

        return context

class SidebarArticlePage(BaseArticlePage):

    date = models.DateField("Post date", default=datetime.date.today)
    order_by_date = models.DateTimeField(default=timezone.now, blank=True, help_text="A date optionally used for ordering. Can be used instead of post date in order to avoid changing the post date")

    parent_page_types = ["SidebarPage"]

    content_panels = Page.content_panels + [


        FieldPanel('body_md'),
        FieldPanel('body_sf'),
        FieldPanel('order_by_date'),
        MultiFieldPanel(
            [
                FieldPanel('document'),
                FieldPanel('show_doc_link'),
            ],
            heading="Document"
        ),
        MultiFieldPanel(
            [
                FieldPanel('embed_url'),
                FieldPanel('embed_frame_style'),
            ],
            heading="Embedded Content"
        ),

    ]

class ArticlePageImage(Orderable):
    page = ParentalKey(
        BaseArticlePage, on_delete=models.CASCADE, related_name='article_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    alt_text = models.TextField("alt text", blank=True, max_length=250)
    display_with_summary = models.BooleanField("with summary", default=False, help_text="If this image should appear where the article summary is shown")
    display_before_body = models.BooleanField("before body", default=False, help_text="If this image should appear before the body of the article")
    display_after_body = models.BooleanField("after_body", default=False, help_text="If this image should appear after the body of the article")
    is_featured = models.BooleanField("is featured", default=False, help_text="If this image is the featured image to be used in social media links and similar contexts. Only one should be selected. ")

    panels = [
        MultiFieldPanel([
            FieldPanel('image'),
            FieldPanel('alt_text'),
        ],
        heading="Image Properties"
        ),
        MultiFieldPanel([
            FieldPanel('display_with_summary'),
            FieldPanel('display_before_body'),
            FieldPanel('display_after_body'),
            FieldPanel('is_featured'),
        ])

    ]

class ArticlePageGalleryImage(Orderable):
    page = ParentalKey(
        BaseArticlePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    alt_text = models.TextField("alt text", blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('alt_text'),
    ]


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'

class ArticleStaticTagsIndexPage(Page):

    show_pagetitle=models.BooleanField( default=True, help_text="If the page title should be shown" )
    included_tag_names_string = models.CharField("tags included", max_length=255, blank=True, help_text="A comma separated list of tags to be included in this page which can also be grouped - separate groups with semicolon")
    tag_titles_string = models.CharField("tag titles", max_length=255, blank=True, help_text="A comma separated list of titles to be used instead of the tag names - not separated by group")
    group_titles_string = models.CharField("group titles", max_length=255, blank=True, help_text="A comma separated list of titles to be used for tag groups")
    apply_special_formatting = models.IntegerField("apply special formatting", default=0, help_text="The group number up to which special formatting should be applied.  Implementation may vary by template app")
    show_body_in_index = models.IntegerField("show body instead of summary", default=0, help_text="The group number up to which articles will show the entire body instead of the summary")
    separate_tag_groups = models.BooleanField(default=True, help_text="If the ArticlePages should be separated by tag")
    show_tag_titles = models.BooleanField(default=True, help_text='If the tag name should be displayed as a title to accompany the ArticlePages')

    order_by_choices=(
        ('-order_by_date','Orderby Date >'),
        ('order_by_date','Orderby Date <'),
        ('-latest_revision_created_at','Update Date/Time >'),
        ('latest_revision_created_at','Update Date/Time <'),
        ('-first_published_at','Publish Date/Time >'),
        ('first_published_at','Publish Date/Time <'),
        ('title','Title'),
        ('-title','Title >'),
    )

    order_by_field = models.CharField(max_length=40,choices=order_by_choices, default=order_by_choices[0], help_text='The article attribute to determine the order in which articles will be displayed')
    content_panels = Page.content_panels + [


        FieldPanel('show_pagetitle'),
        MultiFieldPanel(
            [
                FieldPanel('included_tag_names_string'),
                FieldPanel('order_by_field'),
                MultiFieldPanel([
                    FieldPanel('tag_titles_string'),
                    FieldPanel('group_titles_string'),
                    FieldPanel('separate_tag_groups'),
                ], heading="Tag Titles"),
                FieldPanel('show_tag_titles'),
                MultiFieldPanel([
                    FieldPanel('show_body_in_index'),
                    FieldPanel('apply_special_formatting'),
                ],heading="First Groups")
            ]
        )
    ]

    def get_context(self, request):

        context = super().get_context(request)

        article_page_groups = []

        included_tag_name_groups = self.included_tag_names_string.split(';')
        tag_titles = re.split(r';|,', self.tag_titles_string ) if self.tag_titles_string > '' else []
        group_titles = re.split(r';|,', self.group_titles_string ) if self.group_titles_string > '' else []

        t = 0
        for g in range(len(included_tag_name_groups)):
            new_article_page_group = {'article_page_sets':[]}
            if len(group_titles) > g:
                if group_titles[g] > '':
                    new_article_page_group['group_title'] = group_titles[g]
            article_page_sets = []
            included_tag_names = included_tag_name_groups[g].split(',')

            for i in range(len(included_tag_names)):
                included_tag_name = included_tag_names[i].strip()
                new_article_page_set={}

                new_article_page_set['article_pages'] = ArticlePage.objects.live().filter(tags__name=included_tag_name).order_by(self.order_by_field)

                if new_article_page_set['article_pages']:
                    new_article_page_set['tagname'] = included_tag_name
                    tag_title = tag_titles[t].strip() if len(tag_titles ) > t  else included_tag_name if not included_tag_name[0] == "_" else " "
                    new_article_page_set['title'] = tag_title
                    article_page_sets.append(new_article_page_set)

                t = t + 1


            if article_page_sets:
                new_article_page_group['article_page_sets']=article_page_sets

                article_page_groups.append(new_article_page_group)


        context['sidebars'] = get_sidebars(request)

        context['article_page_groups'] = article_page_groups
        # context['first_group_is_special'] = self.first_group_is_special

        return context

@register_setting
class SiteSpecificImportantPages(BaseSiteSetting):
    article_index_page = models.ForeignKey(
        'wagtailcore.Page', null=True, on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('article_index_page'),
    ]

@register_setting
class SiteTemplateSettings(BaseSiteSetting):

    header_style = models.CharField(
        max_length=255,
        blank=True,
        default="50%",
        help_text="Inline styling for the header",
    )

    banner_image = models.ForeignKey(
        'wagtailimages.Image', related_name='+',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL
    )
    show_banner_image = models.BooleanField(
        'show banner image',
        default=True,
        help_text="Show the chosen banner image.  If deselected, banner_text will be used instead of the image"
    )
    banner_image_style = models.CharField(
        max_length=255,
        blank=True,
        default="50%",
        help_text="Styling for the banner image or if a single value, A css value representing the width of the banner image. Include at least one semicolon (;) to indicate that this is a style, and not just a width value"
    )
    banner_text = models.CharField(
        "banner_text",
        max_length=80,
        blank=True,
        default="webikwa",
        help_text="The alt text to be displayed if there is a banner image, or the text to be displayed if there is no image"
    )
    site_description=models.CharField(
        "site description",
        max_length=80,
        blank=True,
        default="New Wibewa Wagtail Blog",
        help_text="The site description to be displayed near the banner image or banner text"
    )
    show_leftbar=models.BooleanField(
        default=False,
        help_text="If the left sidebar should be shown - requires a template named wibewa/includes/sidebarleft.html"
    )
    show_rightbar=models.BooleanField(
        default=False,
        help_text="If the right sidebar should be shown - requires a template named wibewa/includes/sidebarright.html"
    )
    mainmenu_location=models.CharField(
        "main menu location",
        max_length=20,
        choices=(("none","None"),("top","Top"),("left","Left"),("right","Right")),
        help_text="The location of the main menu",
        default="top"
    )
    theme_color=models.CharField(
        "theme color",
        max_length=30,
        default="black",
        help_text='The theme color. This should match the base name of a css file in a static folder webikwa/css. Ex "blue" if there is a webikwa/css/blue.css'
    )
    footer_text=models.CharField(
        "footer text",
        max_length=255,
        blank=True,
        default="Created wth Wagtail and webikwa",
        help_text="The footer text.  This may be split into a list using footer_text_separator",
    )
    footer_text_separator=models.CharField(
        "footer text separator",
        max_length=2,
        blank=True,
        default=';',
        help_text="The character by which the footer text will be split into a list.  This is optional"
    )
    favicon = models.CharField(
        'path to favicon',
        max_length=125,
        blank=True,
        help_text="The path to the favicon. If static, precede with 'static:' ex: static:images/favicon.ico",
    )

    def __str__(self):
        return "Template Settings for " + self.site.__str__() if self.site is not None else "None"

    class Meta():
        verbose_name_plural = "Template Settings"

def clean_form(self):

    honeypot_err = False

    for field_name in self.honeypot_field_list:
        field_data = self.cleaned_data.get(field_name)
        if str(field_data) > '':
            honeypot_err = True

    if honeypot_err:
        self.add_error(None, self.honeypot_error_message)

    return self.cleaned_data

class FormPage(AbstractEmailForm):

    # h/t: https://github.com/octavenz/wagtail-snippets/blob/master/form-builder-field-validation.md for explanatin of get_form and use of the descriptor

    def get_form(self, *args, **kwargs):

        form = super().get_form(*args, **kwargs)
        form.honeypot_error_message=self.honeypot_error_message

        raw_honeypot_field_list = [ get_field_clean_name(field_label) for field_label in self.honeypot_field_names.split(',') ]
        honeypot_field_list=[]

        self.honeypot_show_intro=False

        for field_name in raw_honeypot_field_list:
            if field_name in form.fields:
                honeypot_field_list.append(field_name)
                self.honeypot_show_intro=True

        form.honeypot_field_list = honeypot_field_list

        form.clean = clean_form.__get__(form)

        form.submission_class = self.get_submission_class()
        form.submission_page = self

        return form


    template = "webikwa/contact_page.html"
    # This is the default path.
    # If ignored, Wagtail adds _landing.html to your template name
    landing_page_template = "webikwa/contact_page_landing.html"

    intro = RichTextField(blank=True, help_text="Enter something like a summary of the form's purpose or general instructions for filling it out. If your form contains honeypots, explain that the form has fields or a field which should be left blank")
    thank_you_text = RichTextField(blank=True, help_text="Enter text to be shown after the form is submitted")

    honeypot_field_names = models.CharField("honeypot", max_length=255, blank=True, help_text="The name or comma-separated list of names for the field or fields to be left blank by humans in order to trap bots. The field(s) should be single-line required=False")
    honeypot_error_message = models.CharField("honeypot error message", max_length=255, blank=True, default="If you are a person, please read the notes and retry", help_text="The name or comma-separated list of names for the field or fields to be left blank by humans in order to trap bots. The field(s) should be single-line required=False")
    honeypot_intro = RichTextField(blank=True, default="Note: This form has a field or fields which should be left unfilled. In order to trap automatic form fillers, these fields are not marked but a person should be able to figure out which those are", help_text="Explain to visitors that the form has a field or fields which humans should realize are to be left blank")

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
        ], heading="Email Settings"),
        MultiFieldPanel([
            FieldPanel("honeypot_field_names"),
            FieldPanel("honeypot_intro"),
            FieldPanel("honeypot_error_message"),
        ], heading="Honeypot")
    ]

class FormField(AbstractFormField):

    page = ParentalKey(FormPage, on_delete=models.CASCADE, related_name='form_fields')

class ArticleCommentPage(Page):
    date = models.DateField("Post date", default=datetime.date.today)
    body = models.CharField(max_length=250, blank=True, help_text='The body of the comment')
    commenter_display_name = models.CharField(max_length=250, blank=True, help_text='The body of the comment')
    in_reply_to = models.ForeignKey("ArticleCommentPage", on_delete=models.SET_NULL,null=True,blank=True)

    parent_page_types = ["ArticlePage"]

    class Meta:
        verbose_name = "Comment"

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('commenter_display_name'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('date'),
                FieldPanel('commenter_display_name', widget=forms.CheckboxSelectMultiple),
            ],
            heading="Article information"
        ),
        FieldPanel('body'),

    ]
