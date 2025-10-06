from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class LimitPagePagination(PageNumberPagination):
    page_size_query_param = 'limit'  # ← заменяем "page_size" на "limit"
    page_query_param = 'page'        # ← стандартное имя для страницы
    max_page_size = 100              # ← максимум за один запрос

    def get_paginated_response(self, data):
        return Response({
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
