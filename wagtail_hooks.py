from wagtail_modeladmin.options import ModelAdmin, modeladmin_register, hooks
from wagtail.admin.viewsets.pages import PageListingViewSet
from .models import ArticlePage, IcalendarPage, SidebarArticlePage
from wagtail.admin.ui.tables import Column
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import Tag


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['webikwa/article.svg']


class ArticlePageListingViewSet(PageListingViewSet):
    icon = "article"
    menu_order = 100  # will put in 3rd place (000 being 1st, 100 2nd)
    menu_label = "Articles"
    add_to_admin_menu = True
    model = ArticlePage
    columns = PageListingViewSet.columns + [Column("get_tags","Tags")]



article_page_listing_viewset = ArticlePageListingViewSet("article_pages")
@hooks.register("register_admin_viewset")
def register_article_page_listing_viewset():
    return article_page_listing_viewset

class SidebarArticlePageListingViewSet(PageListingViewSet):
    icon = "article"
    menu_order = 110  # will put in 3rd place (000 being 1st, 100 2nd)
    menu_label = "Sidebar Articles"
    add_to_admin_menu = True
    model = SidebarArticlePage


sidebar_article_page_listing_viewset = SidebarArticlePageListingViewSet("sidebar_article_pages")
@hooks.register("register_admin_viewset")
def register_sidebar_article_page_listing_viewset():
    return sidebar_article_page_listing_viewset

class IcalendarPageListingViewSet(PageListingViewSet):
    icon = "calendar"
    menu_order = 110  # will put in 3rd place (000 being 1st, 100 2nd)
    menu_label = "Calendars"
    add_to_admin_menu = True
    model = IcalendarPage


icalendar_page_listing_viewset = IcalendarPageListingViewSet("Icalenda_pages")
@hooks.register("register_admin_viewset")
def register_icalendar_page_listing_viewset():
    return icalendar_page_listing_viewset


class TagsSnippetViewSet(SnippetViewSet):
    panels = [FieldPanel("name")]  # only show the name field
    model = Tag
    icon = "tag"  # change as required
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ["name", "slug"]
    search_fields = ("name",)

register_snippet(TagsSnippetViewSet)
