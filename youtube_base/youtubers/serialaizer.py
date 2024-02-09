from rest_framework import serializers

from .models import Youtuber


class YoutuberSerializer(serializers.ModelSerializer):
    """
    Serializer for the Youtuber model.

    This serializer converts complex data types, like Youtuber instances, into Python native
    datatypes that can then be easily rendered into JSON, XML or other content types. It also
    deserializes the received data back into complex types, after validating the received data.

    The fields '__all__' in Meta class indicates that all fields in the Youtuber model should be
    used.

    Attributes:
        model (Model): The model the serializer is tied to, in this case, the Youtuber model.
        fields (str): The fields from the model to be serialized. '__all__' to include all fields.

    """
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Youtuber
        fields = '__all__'

    def get_absolute_url(self, obj):
        print(obj.get_absolute_url, 'qaqwsdqwdewdfewf')
        return obj.get_absolute_url()
