from django.contrib import admin
from .models import Movie, Actor, Review

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display  = ("id", "first_name", "last_name")
    search_fields = ("first_name", "last_name")

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display  = ("id", "title")
    search_fields = ("title", "description")
    filter_horizontal = ("actors",)  # UI pratique pour sélectionner plusieurs acteurs

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ("id", "movie", "grade")
    list_filter   = ("grade",)
    search_fields = ("movie__title",)
