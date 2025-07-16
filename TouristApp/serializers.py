from rest_framework import serializers
from .models import Places,Images


from rest_framework import serializers
from .models import Places, Images

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return ""

    class Meta:
        model = Images
        fields = ['image']
class PlacesSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )
    image_list = serializers.SerializerMethodField()

    class Meta:
        model = Places
        fields = ["id", "name", "wheather", "state", "district", "googlemaplink", "images", "image_list"]

    def create(self, validated_data):
        image_files = validated_data.pop('images')
        place = Places.objects.create(**validated_data)
        for image in image_files:
            Images.objects.create(place=place, image=image)
        return place
    
    def get_image_list(self, obj):  # ✅ MUST BE INSIDE THE CLASS
        request = self.context.get('request')
        return ImageSerializer(obj.images.all(), many=True, context={'request': request}).data
