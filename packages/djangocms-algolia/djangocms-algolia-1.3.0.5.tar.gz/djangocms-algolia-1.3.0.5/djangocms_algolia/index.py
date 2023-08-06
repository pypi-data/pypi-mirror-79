from datetime import datetime
from typing import Union

from aldryn_search.search_indexes import TitleIndex
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from cms.models import Title
from cms.test_utils.testcases import BaseCMSTestCase
from cms.toolbar.toolbar import CMSToolbar
from django.conf import settings
from django.db.models import QuerySet
from django.forms import Media
from django.http import HttpRequest
from django.test import Client
from django.utils import translation
from haystack.indexes import SearchIndex


class FakeCMSRequestFactor(BaseCMSTestCase):
    client = Client
    
    def get_request(self, *args, **kwargs) -> HttpRequest:
        request = super().get_request(*args, **kwargs)
        request.placeholder_media = Media()
        request.session = {}
        request.toolbar = CMSToolbar(request)
        return request


class AlgoliaPageDataProxy(Title):

    class Meta:
        proxy = True

    def search_index_description(self) -> str:
        aldryn_haystack_index: Union[SearchIndex, TitleIndex] = TitleIndex()
        page_content: str = aldryn_haystack_index.get_search_data(
            obj=self,
            language=translation.get_language(),
            request=FakeCMSRequestFactor().get_request(),
        )
        if settings.ALGOLIA_SEARCH_INDEX_TEXT_LIMIT:
            return page_content[:settings.ALGOLIA_SEARCH_INDEX_TEXT_LIMIT]
        else:
            return page_content

    def pub_date(self) -> datetime:
        return self.page.publication_date

    def url(self) -> datetime:
        return self.page.get_absolute_url()


@register(AlgoliaPageDataProxy)
class PageIndex(AlgoliaIndex):
    index_name = 'cms_pages'
    
    fields = [
        'title',
        'url',
        'pub_date',
        'meta_description',
        'search_index_description',
    ]

    def get_queryset(self) -> QuerySet:
        aldryn_haystack_index: SearchIndex = TitleIndex()
        return aldryn_haystack_index.get_index_queryset(
            language=translation.get_language(),
        )

    def get_settings(self) -> dict:
        lang_code_current: str = translation.get_language()
        snippet_limit = getattr(settings, 'ALGOLIA_SEARCH_DESC_SNIPPET_LIMIT', 40)
        return {
            'indexLanguages': [lang_code_current],
            'queryLanguages': [lang_code_current],
            'ignorePlurals': [lang_code_current],
            'removeStopWords': [lang_code_current],
            'attributesToSnippet': [
                f'*:{snippet_limit}',
            ],
            'snippetEllipsisText': '...',
            'highlightPreTag': '<b>',
            'highlightPostTag': '</b>',
        }
