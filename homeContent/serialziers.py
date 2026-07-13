from rest_framework import serializers

from homeContent.models import Show, TeamMember




class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"