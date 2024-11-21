from django.db.models import Model
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            # 'access': str(refresh.access_token),
            # 'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance. username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = 'all'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = 'all'


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = 'all'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = 'all'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = 'all'


class MovieListSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True, many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'genre', 'country', 'average_rating', 'year']

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class MovieDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True, many=True)
    director = DirectorSerializer(read_only=True, many=True)
    actor = ActorSerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True, many=True)
    average_rating = serializers.SerializerMethodField()
    ratings = RatingSerializer(read_only=True, many=True)


    class Meta:
        model = Movie
        fields = ['movie_name', 'country', 'director', 'actor', 'genre', 'types', 'description', 'movie_time',
                  'average_rating','movie_trailer', 'movie_image', 'ratings', 'year', 'status_movie']


    def get_average_rating(self, obj):
        return obj.get_average_rating()

class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), write_only=True, source='movie')


    class Meta:
        model = Favorite
        fields = ['id', 'movie', 'movie_id']


class FavoriteMovieSerializer(serializers.ModelSerializer):
    items = FavoriteSerializer(read_only=True, many=True)


    class Meta:
        model = FavoriteMovie
        fields = ['id', 'user', 'items']