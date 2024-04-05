from rest_framework import serializers


class DoctorCheckSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    reg_num = serializers.IntegerField()
