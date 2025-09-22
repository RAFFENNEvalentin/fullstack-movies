from rest_framework import serializers
from .models import Actor, Movie, Review

# Déjà présent
class HealthSerializer(serializers.Serializer):
    status = serializers.CharField()


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class MovieSerializer(serializers.ModelSerializer):
    # lecture
    actors = ActorSerializer(many=True, read_only=True)
    average_grade = serializers.FloatField(read_only=True)

    # écriture: on passe des IDs d'acteurs
    actor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "description",
            "actors", 
            "average_grade",
            "actor_ids", 
        )

    def update(self, instance, validated_data):
        actor_ids = validated_data.pop("actor_ids", None)
        instance = super().update(instance, validated_data)
        if actor_ids is not None:
            instance.actors.set(actor_ids)
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("grade",)
        # Important : les validators (1..5) définis sur le modèle
        # sont automatiquement appliqués par DRF -> 400 si invalide.