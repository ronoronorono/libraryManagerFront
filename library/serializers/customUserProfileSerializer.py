from rest_framework import serializers

from library.models import CustomUserProfile

class CustomUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserProfile
        fields = ('id', 'username', 'library_card_number', 'updated_at', 'is_staff', 'is_superuser', 'first_name', 'last_name', 'email')

    def validate(self, data):
        user = self.context['request'].user
        if not user.is_staff:
            allowed_fields = ['first_name', 'last_name', 'password', 'email']
            for field in data.keys():
                if field not in allowed_fields:
                    raise serializers.ValidationError("You are not allowed to change this field.")
        return data