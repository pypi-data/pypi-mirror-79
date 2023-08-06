import json
import logging

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from remo_app.remo.models.downloads import AgrInstallations

logger = logging.getLogger('remo_app')


class ValidateUUID(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        return Response({})

    @staticmethod
    def parse_payload(request):
        try:
            data = json.loads(request.body)
        except Exception:
            return Response({'error': 'failed to parse payload'}, status=status.HTTP_400_BAD_REQUEST), None

        return None, data

    def create(self, request, *args, **kwargs):
        err, data = self.parse_payload(request)
        if err:
            return err

        uuid = data.get('uuid')
        if not uuid:
            return Response({'error': 'failed to parse uuid'},
                            status=status.HTTP_400_BAD_REQUEST)

        result = {'valid': AgrInstallations.objects.filter(uuid=uuid).exists()}
        return Response(result, status=status.HTTP_200_OK)

