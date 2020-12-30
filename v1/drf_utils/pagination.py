# -*- encoding: utf-8 -*-
"""
@File    : pagination.py
@Time    : 2020/12/30 14:32
@Author  : wuhao
"""

from rest_framework import pagination
from rest_framework.response import Response

class PageNumberPagination(pagination.PageNumberPagination):
        max_page_size = 9999999
        page_size_query_param = 'limit'
        page_query_description = '页数'
        page_size_query_description = '每页限定行数'
        invalid_page_message = '已经没有更多了'

        def get_paginated_response(self, data):
            page_size = self.get_page_size(self.request)
            return Response({
                'paging': {
                    'limit': page_size,
                    'skip': (self.page.number-1)*page_size,
                    'total': min(self.page.paginator.count, self.max_page_size),
                    'page': self.page.number,
                    'total_pages': self.page.paginator.num_pages,
                    },
                'results': data
            })