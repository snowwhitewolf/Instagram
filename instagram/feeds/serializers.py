from rest_framework import serializers

from .models import FeedImage, Feed, FeedComment


class FeedImageSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = FeedImage
        fields = ['image']


class FeedSerializer(serializers.ModelSerializer):

    images = FeedImageSerializer(many=True, read_only=True)


    class Meta:
        model = Feed
        fields = ['id', 'title', 'content', 'date_created', 'images']
        
        
    def create(self, validated_data):
        instance = Feed.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            FeedImage.objects.create(feed=instance, image=image_data)
        return instance

# class FeedSerializer(serializers.ModelSerializer):
#     images = serializers.SerializerMethodField()

#     def get_images(self, obj):
#         image = obj.diaryimage_set.all()
#         return FeedImageSerializer(instance=image, many=True).data

#     class Meta:
#         model = Feed
#         fields = ['id', 'title', 'content', 'date_created', 'images']

#     def create(self, validated_data):
#         instance = Feed.objects.create(**validated_data)
#         image_set = self.context['request'].FILES
#         for image_data in image_set.getlist('image'):
#             FeedImage.objects.create(feed=instance, image=image_data)
#         return instance