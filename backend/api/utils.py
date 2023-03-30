from recipes.models import Ingredient, IngredientInRecipe


def create_update_ingredients_in_recipe(recipe, ingredients):
    """Изменение ингредиентов в рецепте"""
    all_ing_in_rec = []
    for ingredient in ingredients:
        current_ingredient = Ingredient.objects.get(id=ingredient['id'])
        amount = ingredient['amount']
        ing_in_rec = IngredientInRecipe(
            ingredient_in_recipe=current_ingredient, recipe=recipe,
            amount=amount
        )
        all_ing_in_rec.append(ing_in_rec)
    IngredientInRecipe.objects.bulk_create(all_ing_in_rec)
