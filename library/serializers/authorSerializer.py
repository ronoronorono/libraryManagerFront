from rest_framework import serializers
from library.models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name','nationality', 'is_active', 'deleted_at', 'inserted_at', 'updated_at')

    def validate(self, data):

        allowed_fields = ['first_name', 'last_name', 'nationality', 'is_active']

        if data['first_name'] is None or data['last_name'] is None:
            raise serializers.ValidationError("This field cannot be blank.")

        for field in data.keys():

            if field not in allowed_fields:
                raise serializers.ValidationError(f"You are not allowed to change this field. {field}")

        return data