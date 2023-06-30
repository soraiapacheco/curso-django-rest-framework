from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tag.models import Tag

from ..models import Recipe
from ..permissions import IsOwner
from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 2


class RecipeAPIV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIV2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    http_method_names = ['get', 'options', 'head', 'patch', 'post', 'delete']

    def get_queryset(self):
        qs = super().get_queryset()
        # print('Parâmetros', self.kwargs)
        # print('Query Strings', self.request.query_params)
        category_id = self.request.query_params.get('category_id', '')
        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)
        # print('Category id:', category_id)

        return qs

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk)

        self.check_object_permissions(self.request, obj)

        return obj

    def list(self, request, *args, **kwargs):
        print('REQUEST: ', request.user, self.request.user)
        print(request.user.is_authenticated)

        return super().list(request, *args, **kwargs)

    # called by post method
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]
        if self.request.method == 'POST':
            return []
        return super().get_permissions()


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request})
    return Response(serializer.data)
