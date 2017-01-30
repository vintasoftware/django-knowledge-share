import re

from django.views import generic
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.apps import apps

from user.models import InfoEmployee

from .twitter_helpers import post_microblog_post_on_twitter


MicroBlogPost = apps.get_model('microblog', 'MicroBlogPost')
MicroBlogCategory = apps.get_model('microblog', 'MicroBlogCategory')


def _normalize_and_split_data(text):
    # Normalize and remove empty spaces.
    content = re.sub('[ ](?=[^\]]*?(?:\[|$))', '', text)
    content = content.replace('][', '][').replace('],[', '][')

    # Remove first and last itens and split the string into a list.
    content = content[1:-1].split('][')
    return content


def _clean_category_name(category_name):
    return category_name.lower().strip()


def _matchUsers(user_name, SLACK_BLOG_USERS):
    return SLACK_BLOG_USERS.get(user_name, user_name)


def _get_author(user_name):
    return InfoEmployee.objects.get(
        user__username=_matchUsers(user_name, settings.SLACK_BLOG_USERS)
    )


class SlackSlashWebHookView(generic.View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        token = request.POST.get('token')
        if not token or token != settings.SLACK_TOKEN:
            response = {
                'response_type': 'in_channel',
                'text': 'Invalid Slack token',
            }
            return JsonResponse(response, status=400)
        return super().dispatch(request, *args, **kwargs)

    def format_response_success_text(self, new_post):
        edit_msg = (
            'Thanks for the post! \n Edit here:'
            '{}/calotebox/microblog/microblogpost/{}'
        ).format(self.request.META['HTTP_HOST'], new_post.id)

        see_post_msg = '\n See here: {}/lessons-learned/{}'.format(
                       self.request.META['HTTP_HOST'], new_post.slug)

        return '{}{}'.format(edit_msg, see_post_msg)

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            text_param = data['text']
            user_name_param = data['user_name']
        except KeyError:
            response = {
                'response_type': 'in_channel',
                'text': 'Invalid/Missing some information',
            }
            return JsonResponse(response, status=400)
        content = _normalize_and_split_data(text_param)
        if len(content) not in [1, 2]:
            text = (
                'Hey, your post failed! \n Make sure that '
                'you used this expression: [Content*][Categories]'
            )
            response = {
                'response_type': 'in_channel',
                'text': text,
            }
            return JsonResponse(response, status=400)
        else:
            try:
                new_post, created = MicroBlogPost.objects.get_or_create(
                    title='',
                    content=content[0],
                    author=_get_author(user_name_param)
                )
                if len(content) == 2:
                    category_post = content[1].split(',')
                    for item in category_post:
                        category_name = _clean_category_name(item)
                        category_item, _ = (
                            MicroBlogCategory.objects.get_or_create(
                                name=category_name))
                        new_post.category.add(category_item)
                if created:
                    post_microblog_post_on_twitter(new_post)
            except ObjectDoesNotExist:
                text = (
                    'Hey, your slack username was not found.'
                )
                response = {
                    'response_type': 'in_channel',
                    'text': text,
                }
                return JsonResponse(response, status=404)
            except IntegrityError:
                text = (
                    'Hey, this post already exists. Try to use a'
                    ' different slug!'
                )
                response = {
                    'response_type': 'in_channel',
                    'text': text,
                }
                return JsonResponse(response)
            else:
                response_text = self.format_response_success_text(new_post)
                response = {
                    'response_type': 'in_channel',
                    'text': response_text
                }
                return JsonResponse(response, status=200)
