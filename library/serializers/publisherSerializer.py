from rest_framework import serializers

from library.models import Publisher

class publisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id', 'publisher_name', 'updated_at', 'is_active','deleted_at')
        read_only_fields = ('id', 'updated_at', 'deleted_at')

    def validate(self, data):
        allowed_fields = ['publisher_name', 'is_active']
        for field in data.keys():
            if field is None:
                raise serializers.ValidationError("This field cannot be blank.")
            if field not in allowed_fields:
                raise serializers.ValidationError(f"You are not allowed to change this field. {field}")
        return data