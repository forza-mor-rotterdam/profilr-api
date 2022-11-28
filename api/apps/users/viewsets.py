from apps.users.models import Profile
from apps.users.serializers import ProfileSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class ProfileViewSet(viewsets.ModelViewSet):

    queryset = Profile.objects.all()

    serializer_class = ProfileSerializer

    http_method_names = [
        "get",
        "post",
    ]

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print(request.META)
        print(request.data)
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
