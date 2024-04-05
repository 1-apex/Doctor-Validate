from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DoctorCheckSerializer
from .views import check


class DoctorCheckAPIView(APIView):
    def post(self, request):
        serializer = DoctorCheckSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            reg_num = serializer.validated_data.get('reg_num')
            content = check(name, reg_num)
            if content:
                return Response({'content': 'Valid'}, status=status.HTTP_200_OK)
            else:
                return Response({'content': 'Invalid'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
