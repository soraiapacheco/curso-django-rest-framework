from collections import defaultdict

from django.contrib.auth.models import User
from rest_framework import serializers

from tag.models import Tag

from .models import Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_links',]

    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(
        source='is_published',
        read_only=True)
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        read_only=True)

    # id of the category
    # in this case, it uses: from .models import Category
    # category = serializers. PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(),
    # )
    # name of the category
    # category_name = serializers.StringRelatedField(
    #     source='category'
    # )
    # or just category
    category = serializers.StringRelatedField()

    # name of the author
    # author = serializers.StringRelatedField()
    # or

    tag_objects = TagSerializer(
        many=True, source='tags'
    )

    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    # def validate(self, attrs):
    #    print('Método validate', attrs)
    #    return super().validate(attrs)

    def validate(self, attrs):
        super_validate = super().validate(attrs)
        title = attrs.get('title')
        description = attrs.get('description')

        if title == description:
            raise serializers.ValidationError({
                'title': 'Cannot be equal to description',
                'description': 'Cannot be equal to title'

            }

            )

        return super_validate

    def validate_title(self, value):
        title = value
        # print('Title:', value, 'Tamanho do title', len(title))

        if len(title) < 5:
            raise serializers.ValidationError('Must have at least 5 chars.')
        return title
