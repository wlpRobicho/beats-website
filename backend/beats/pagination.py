from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class BeatPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': math.ceil(self.page.paginator.count / self.page_size),
            'current_page': self.page.number,
            'page_size': self.page.paginator.per_page,
            'results': data
        })
