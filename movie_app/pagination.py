from rest_framework.pagination import PageNumberPagination


class MoviePagination(PageNumberPagination):
    page_size = 5

class CategoryPagination(PageNumberPagination):
    page_size = 4

class GenrePagination(PageNumberPagination):
    page_size = 6
