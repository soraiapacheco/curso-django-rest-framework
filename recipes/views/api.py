from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Recipe
from ..serializers import RecipeSerializer


# @api_view(http_method_names=['get', 'post'])
@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()[:10]
    serializer = RecipeSerializer(instance=recipes, many=True)
    return Response(serializer.data)


@api_view()
def recipe_api_detail(request, pk):
    # recipe = Recipe.objects.filter(pk=pk).first()

    # to use the object 404
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serializer = RecipeSerializer(instance=recipe)
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
