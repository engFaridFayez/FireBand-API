from rest_framework import viewsets
from rest_framework import permissions

from homeContent.models import Show, TeamMember
from homeContent.serialziers import ShowSerializer, TeamSerializer
# Create your views here.
class ShowViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class TeamViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = TeamMember.objects.all()
    serializer_class = TeamSerializer