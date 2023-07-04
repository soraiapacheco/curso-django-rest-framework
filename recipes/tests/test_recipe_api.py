from rest_framework import test

from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIV2Test(test.APITestCase, RecipeMixin):
    def test_the_test(self):
        assert 1 == 1
