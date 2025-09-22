from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)

    class Meta:
        ordering = ("last_name", "first_name")

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

class Movie(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # 1 acteur ⇄ plusieurs films ET 1 film ⇄ plusieurs acteurs  → ManyToMany
    actors      = models.ManyToManyField(Actor, related_name="movies", blank=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    # Le sujet parle de "grade" (1..5). On respecte le nom exact.
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        ordering = ("id",)