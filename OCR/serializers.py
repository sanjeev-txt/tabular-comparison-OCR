from rest_framework import serializers

class ImagePathSerializer(serializers.Serializer):
    document_path = serializers.FileField(required=True)
    specific_path = serializers.FileField(required=True)
    