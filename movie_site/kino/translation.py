from .models import *
from modeltranslation.translator import TranslationOptions,register

@register(Movie)
class ProductTranslationOptions(TranslationOptions):
    fields = ('movie_name', 'description')


@register(Country)
class ProductTranslationOptions(TranslationOptions):
    fields = ('country_name',)


@register(Director)
class ProductTranslationOptions(TranslationOptions):
    fields = ('director_name', 'biography')

@register(Actor)
class ProductTranslationOptions(TranslationOptions):
    fields = ('actor_name', 'biography')

@register(Genre)
class ProductTranslationOptions(TranslationOptions):
    fields = ('genre_name',)

@register(Rating)
class ProductTranslationOptions(TranslationOptions):
    fields = ('text',)