import datetime
import re
import misaka

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_markdown.models import MarkdownField
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from knowledge_share.conf import KNOWLEDGE_APP_NAME


class MicroBlogCategoryBase(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _("categories")
        abstract = True

    @property
    def hashtag(self):
        joined_name = ''.join(self.name.title().split())
        return '#{}'.format(joined_name)

    def __str__(self):
        return self.name


class MicroBlogPostBase(models.Model):
    title = models.CharField(
        blank=True,
        max_length=100,
        verbose_name=_('Title')
    )
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        blank=True,
        db_index=True,
        unique=True
    )
    content = MarkdownField()
    pub_date = models.DateTimeField(verbose_name=_('date published'))
    # This should be 'categories' but keeping it for backward compatibility
    category = models.ManyToManyField(KNOWLEDGE_APP_NAME + '.MicroBlogCategory')
    posted_on_twitter = models.BooleanField(default=False)

    class Meta:
        abstract = True
        verbose_name_plural = _("posts")

    def content_to_slug(self, content):
        new_slug = re.sub('<[^<]+?>', '', misaka.html(content))
        new_slug = new_slug.split()
        new_slug = '-'.join(new_slug[:6])

        return new_slug

    def get_absolute_url(self):
        return reverse(KNOWLEDGE_APP_NAME + ':microblog-post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.content_to_slug(self.content))
            self.pub_date = datetime.datetime.now()
        super(MicroBlogPostBase, self).save(*args, **kwargs)
