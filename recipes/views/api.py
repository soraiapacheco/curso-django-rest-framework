from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


# @api_view(http_method_names=['get', 'post'])
@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.validated_data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def recipe_api_detail(request, pk):
    # recipe = Recipe.objects.filter(pk=pk).first()

    # to use the object 404
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serializer = RecipeSerializer(
        instance=recipe,
        many=False,
        context={'request': request})
    return Response(serializer.data)

    # or another way changing the message
    # it is necessary import: from rest_framework import status
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()
    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe)
    #     return Response(serializer.data)
    # else:
    #     # Put of way hard code
    #     # return Response({
    #     #    'detail': 'Eita',
    #     # }, status=404)
    #     return Response({
    #         'detail': 'Eita',
    #     }, status=status.HTTP_418_IM_A_TEAPOT)


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
