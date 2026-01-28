from django.contrib.sitemaps import Sitemap

from student.models import Student


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Student.published.all()


    def lastmod(self, obj):
        return obj.time_update