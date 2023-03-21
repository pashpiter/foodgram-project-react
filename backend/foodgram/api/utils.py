from recipes.models import RecipeList, IngridientInRecipe, Ingridient

def UpdateIngridientsInRecipe(recipe, ingridients):
    for ingridient in ingridients:
        current_ingridient = Ingridient.objects.get(id=ingridient['id'])
        IngridientInRecipe.objects.create(
            ingridient_in_recipe=current_ingridient, recipe=recipe,
            amount=ingridient['amount']
        )
    
    recipe.ingridients.add(
                current_ingridient,
                through_defaults={'amount': ingridient['amount']}
            )