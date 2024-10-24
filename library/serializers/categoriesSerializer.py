from rest_framework import serializers

from library.models import Category

class categoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'updated_at', 'is_active')

    def validate(self, data):

        allowed_fields = ['name', 'description', 'is_active']

        for field in data.keys():

            if field is None:
                raise serializers.ValidationError("This field cannot be blank.")
            if field not in allowed_fields:
                raise serializers.ValidationError(f"You are not allowed to change this field. {field}")
        return data