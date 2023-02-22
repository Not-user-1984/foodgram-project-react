from rest_framework.pagination import PageNumberPagination


class PageCastomNumberPagition(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 20


class NoNumberPagition(PageNumberPagination):
    page_size = None
    page_size_query_param = None
    max_page_size = None
