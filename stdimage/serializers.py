from rest_framework import serializers


class StdImageSerializer(serializers.ImageField):
    """Serializer for StdImageField that returns URLs for all variations."""

    def to_representation(self, obj):
        if not obj:
            return None
        return self._get_variation_urls(obj)

    def _get_variation_urls(self, obj):
        result = {}

        # Original image first
        if hasattr(obj, "url"):
            result["original"] = super().to_representation(obj)

        # Each registered variation
        field = obj.field
        if hasattr(field, "variations"):
            for key in field.variations:
                variation = getattr(obj, key)
                if variation and hasattr(variation, "url"):
                    result[key] = super().to_representation(variation)

        return result
