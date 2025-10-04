import re

from django.db.models import Count, Q, Case, When, IntegerField, Value
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.services.classifier.model_loader import classifier
from apps.item.models import Keyword, Item
from apps.item.serialziers.item import ItemSerializer


class ItemSearchView(APIView):
    """
    Search items by keywords with intelligent ranking.

    Query params:
        q: search query string
        limit: max results (default: 20)
    """

    STOPWORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for',
        'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on',
        'that', 'the', 'to', 'was', 'will', 'with'
    }

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        limit = int(request.query_params.get('limit', 20))

        if not query:
            return Response(
                {"error": _("Search query is required")},
                status=status.HTTP_400_BAD_REQUEST
            )

        tokens = self._tokenize(query)

        if not tokens:
            return Response(
                {"results": [], "query": query, "tokens": []},
                status=status.HTTP_200_OK
            )

        matching_keywords = Keyword.objects.filter(
            name__in=tokens
        ).values_list('id', 'name')

        keyword_ids = [kw[0] for kw in matching_keywords]
        matched_token_names = {kw[1] for kw in matching_keywords}

        if not keyword_ids:
            return Response(
                {
                    "results": [],
                    "query": query,
                    "tokens": tokens,
                    "message": _("No items found matching the search terms")
                },
                status=status.HTTP_200_OK
            )

        items = self._search_and_rank_items(
            tokens, keyword_ids, matched_token_names, limit
        )

        serializer = ItemSerializer(items, many=True)

        return Response({
            "results": serializer.data,
            "query": query,
            "tokens": tokens,
            "matched_tokens": list(matched_token_names),
            "total_results": len(items)
        })

    def _tokenize(self, query):
        """
        Tokenize and normalize the search query.

        Steps:
        1. Lowercase
        2. Split by whitespace and punctuation
        3. Remove stopwords
        4. Remove empty strings
        """

        query = query.lower()

        tokens = re.findall(r'\b\w+\b', query)

        tokens = [
            token for token in tokens
            if token and token not in self.STOPWORDS and len(token) > 1
        ]

        seen = set()
        unique_tokens = []
        for token in tokens:
            if token not in seen:
                seen.add(token)
                unique_tokens.append(token)

        return unique_tokens

    def _search_and_rank_items(self, tokens, keyword_ids, matched_token_names, limit):
        """
        Search items and rank by relevance.

        Ranking factors:
        1. matched_terms_count: How many distinct query tokens matched
        2. exact_title_match: Does the title contain the exact query
        3. total_keywords: Total number of keywords (popularity signal)
        """

        items_qs = Item.objects.filter(
            item_keywords__keyword_id__in=keyword_ids
        ).distinct()

        matched_terms_annotations = {}
        for i, kw_id in enumerate(keyword_ids):
            matched_terms_annotations[f'has_kw_{i}'] = Case(
                When(item_keywords__keyword_id=kw_id, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )

        items_qs = items_qs.annotate(**matched_terms_annotations)

        matched_count_sum = sum([
            f'has_kw_{i}' for i in range(len(keyword_ids))
        ], Value(0))

        items_qs = items_qs.annotate(
            matched_terms_count=Count('item_keywords__keyword', distinct=True,
                                      filter=Q(item_keywords__keyword_id__in=keyword_ids))
        )

        title_match_conditions = []
        for token in tokens:
            title_match_conditions.append(
                When(title__icontains=token, then=Value(1))
            )

        items_qs = items_qs.annotate(
            exact_title_match=Case(
                *title_match_conditions,
                default=Value(0),
                output_field=IntegerField()
            )
        )

        items_qs = items_qs.annotate(
            total_keywords_count=Count('item_keywords', distinct=True)
        )

        items_qs = items_qs.order_by(
            '-matched_terms_count',
            '-exact_title_match',
            '-total_keywords_count',
            'title'
        )

        return items_qs[:limit]


class ItemSearchViewPostgreSQL(APIView):
    """
    Advanced search using PostgreSQL Full-Text Search.
    Requires PostgreSQL database.
    """

    def get(self, request):
        from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

        query = request.query_params.get('q', '').strip()
        limit = int(request.query_params.get('limit', 20))

        if not query:
            return Response(
                {"error": _("Search query is required")},
                status=status.HTTP_400_BAD_REQUEST
            )

        search_vector = (
                SearchVector('title', weight='A') +
                SearchVector('item_keywords__keyword__name', weight='B')
        )

        search_query = SearchQuery(query)

        items = Item.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(
            search=search_query
        ).order_by('-rank')[:limit]

        serializer = ItemSerializer(items, many=True)

        return Response({
            "results": serializer.data,
            "query": query,
            "total_results": len(items)
        })
