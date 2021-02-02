from rest_framework import serializers

from helper import keys
from helper.views import HelperCommon
from main.models import UserData


class UserDataSerializer(serializers.ModelSerializer):
    """
    User profile data
    """
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    def get_email(self, instance):
        return instance.email if instance.email is not None and instance.email is not '' else ''

    def get_mobile(self, instance):
        return instance.mobile if instance.mobile is not None and instance.mobile is not '' else ''

    def get_created(self, instance):
        return HelperCommon.convert_utc_to_local_timezone(instance.created). \
            strftime(keys.DATE_FORMAT_d_b_Y + ", " + keys.TIME_FORMAT_H_M_AM_PM)

    class Meta:
        model = UserData
        fields = ['email', 'mobile', 'username', 'created']
