from django.apps import apps
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from knowledge_share.conf import KNOWLEDGE_APP_NAME, KNOWLEDGE_USE_TWITTER
from knowledge_share.exceptions import BadRequest
from knowledge_share.twitter_helpers import post_microblog_post_on_twitter
from tapioca.exceptions import ClientError

MicroBlogPost = apps.get_model(KNOWLEDGE_APP_NAME, 'MicroBlogPost')
MicroBlogCategory = apps.get_model(KNOWLEDGE_APP_NAME, 'MicroBlogCategory')


def _normalize_and_split_data(text):
    # Remove first and last itens and split the string into a list.
    text = text.strip()
    last_open_sqbra = text.rfind('[')
    message = text
    categories_str = ''
    if text.endswith(']') and last_open_sqbra != -1:
        categories_str = text[last_open_sqbra + 1:-1]
        message = text[:last_open_sqbra]
    return message.strip(), categories_str


def _clean_category_name(category_name):
    return category_name.lower().strip()


class SlackSlashWebHookView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        token = request.POST.get('token')
        try:
            if not token or token != settings.SLACK_TOKEN:
                raise BadRequest('Invalid Slack token')

            return super(SlackSlashWebHookView, self).dispatch(request, *args, **kwargs)
        except BadRequest as e:
            return self.bad_request(e.message)

    def format_response_success_text(self, new_post, twitter_error):
        edit_msg = (
            'Thanks for the post! {}\n'
        ).format(
            '(it worked! But twitter posting failed)' if twitter_error else '')

        return edit_msg

    def get_params(self, **kwargs):
        data = self.request.POST
        kwargs['text_param'] = data['text']
        return kwargs

    def bad_request(self, text):
        response = {
            'response_type': 'in_channel',
            'text': text,
        }
        return JsonResponse(response, status=400)

    def get_or_create_microblogpost(self, params, categories, **kwargs):
        new_post, created = MicroBlogPost.objects.get_or_create(
            **kwargs
        )
        if categories:
            category_post = categories.split(',')
            for item in category_post:
                category_name = _clean_category_name(item)
                category_item, _ = (
                    MicroBlogCategory.objects.get_or_create(
                        name=category_name))
                new_post.category.add(category_item)
        return new_post, created

    def post(self, request, *args, **kwargs):
        try:
            params = self.get_params()
        except KeyError:
            raise BadRequest('Invalid/Missing some information')

        try:
            content, categories = _normalize_and_split_data(params['text_param'])
        except ValueError:
            text = (
                'Hey, your post failed! \n Make sure that '
                'you used this expression: Content [Categories]'
            )
            raise BadRequest(text)

        new_post, created = self.get_or_create_microblogpost(params, categories,
                                                             content=content, title='')
        try:
            if created and KNOWLEDGE_USE_TWITTER:
                post_microblog_post_on_twitter(new_post)
        except ClientError:
            twitter_error = True
        else:
            twitter_error = False
        response_text = self.format_response_success_text(new_post, twitter_error)
        response = {
            'response_type': 'in_channel',
            'text': response_text
        }
        return JsonResponse(response, status=200)


class MicroblogPostView(DetailView):
    model = MicroBlogPost
    template_name = KNOWLEDGE_APP_NAME + '/microblog_post.html'
