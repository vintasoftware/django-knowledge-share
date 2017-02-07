from django.db import models

from vinta_microblog import models as microblog_abstract_models


class MicroBlogPost(microblog_abstract_models.MicroBlogPostBase):
    pass


class MicroBlogCategory(microblog_abstract_models.MicroBlogCategoryBase):
    pass
