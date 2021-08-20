from django.contrib import admin

from .models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    fk_name = 'recipe'


class TagsRecipeInline(admin.TabularInline):
    model = TagRecipe
    fk_name = 'recipe'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_ingridients', 'get_tags',
                    'name', 'text', 'cooking_time', 'author', )
    search_fields = ('name',)

    inlines = [
        IngredientRecipeInline,
        TagsRecipeInline,
    ]

    def get_ingridients(self, obj):
        return (" ".join([item.name for item in obj.ingredients.all()]))
    get_ingridients.short_description = 'Ингредиенты'

    def get_tags(self, obj):
        return "\n".join([item.slug for item in obj.tags.all()])
    get_tags.short_description = 'Тэги'


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('slug',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
