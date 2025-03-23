# Webikwa

Webikwa is a blog app for Wagtail

## Important Note

This project is in development and there may be breaking changes until this note is removed

## Installation

Webikwa requires webikwa_base, touglates and wagtail_modeladmin. If you're using a different template app than webikwa_base, you can substitute that app

These instructions are written with the assumption that you're starting a new project

* create a new Wagtail project (see [Wagtail's instructions](https://docs.wagtail.org/en/v6.2.1/getting_started/) )
* pip install [wagtail-markdown](https://pypi.org/project/wagtail-markdown/)
* pip install [wagtail_modeladmin](https://pypi.org/project/wagtail-modeladmin/)
* git clone [https://github.com/tougshire/touglates](https://github.com/tougshire/touglates)
* git clone [https://github.com/tougshire/webikwa_base](https://github.com/tougshire/webikwa_base)
* git clone [https://github.com/tougshire/webikwa](https://github.com/tougshire/webikwa)
* add the following to INSTALLED_APPS:
    * "wagtail.contrib.settings"
	* "wagtail_modeladmin"
    * "wagtailmarkdown"
    * "wagtail.contrib.table_block",
	* "touglates"
	* "webikwa_base"
	* "webikwa"
* Add the following to your settings:
```
WAGTAILMARKDOWN = {
    "autodownload_fontawesome": True,
    "extensions": ['extra'],
}
```
* run the migrations again
* run collectstatic


## Setting Up Tutorial

### Basic setup making use of a featured article page and a redirect page

* run the server (python manage.py runserver) and browse to the admin panel (127.0.0.1:8000/admin
* rename the automatically-created page
    * in the admin panel, click "Pages", then the edit icon (a pencil) for the automatically created page (which may be "home" or "welcome or something like that)
    * If the title of the page is "Home", change the title to "Home-Old".
	In the promote tab, rename the slug from "home" to "home-old".
    * publish the page
* create a new article index page
    * using the "add child page" action next to the word "Root", create a new article index page
    * name it "Articles"
    * publish the page
* create a new article static tags index page
    * from the root page, create a new article static tags index page
    * name it "Featured Articles"
    * under "tags included" enter "_f1,_f2;_f3,_f4;_f5" (don't include quotation marks a any point unless specified)
	* under "show body instead of summary", enter 1
    * publish the page
* create a new redirect page
    * from root, create a new redirect page
    * name it "Home"
    * for the target page, choose the featured articles page
    * publish the page
* move the featured articles page and the articles index page under the home page
    * from the page list under root, check the checkboxes next to Featured Articles and Articles
    * click the "move" button
    * click the three dots next to "Root" and "Choose another page"
    * choose Home
	* Click "Yes, move these pages"
* make Home the root page for the default site
    * click "Settings" then "Sites"
    * choose the default site (probably the only site, "localhost")
	* change the root page from the old home page to the new home page (which is the redirect page)
	* publish the change

### Adding featured articles

* Add articles by clicking "Articles" in the sidebar. Tag each with one of "_f1", "_f2", "_f3", or ""_f4".  Publish each article
	* Note that because _f1 and _f2 are both in the first tag group (you grouped tags with with semicolons in an earlier step), and because "show body instead of summary" was 1, the entire body is shown instead of the summary for articles with those tags

### Adding sidebar articles
* Create a single tag page
	* Click "Pages" from the side menu, then "Home"
	* Click the icon to add a page and and choose "Article Static Tags Index Page"
	* For "title" type "About"
	* For "tags included" type "about"
* Create a sidebar page
	* From the admin sidebar, click "Pages" then "Home"
	* Click the icon for a new page, then choose "Sidebar page"
	* For the title, type "Left Sidebar"
	* Uncheck "Show pagetitle"
	* For location, choose "Left"
	* Save the page
* Enable the sidebar
	* In the admin sidebar, click "Settings", then "Site Template Settings"
	* Check "Show leftbar"
	* Save the settings
* Create a sidebar menu
	* Click "Sidebar Articles" then "Add Sidebar Article Page"
	* For "Page Title" type "Main Menu"
	* In "Body md" type the following:
```markdown
* [home](/)
* [about](/about)
```
*	* publish the page
* Create an article with the "About" Tag
	* Click "Articles", then "Add an article"
	* For the title type "About me"
	* For tags, type "about"
	* Type anyth appropriate for summary and body
	* Publish the page
* Visit the site and check the menu

