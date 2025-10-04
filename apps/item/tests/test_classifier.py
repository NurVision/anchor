from rest_framework import serializers, generics
from rest_framework.response import Response
from rest_framework import status
from apps.common.services.classifier.model_loader import classifier


class TestClassifierSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
    choices = serializers.CharField(required=True)


class TestClassifierView(generics.GenericAPIView):
    serializer_class = TestClassifierSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.query_params)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        query = serializer.validated_data['query']
        choices = serializer.validated_data['choices']

        choices_list = [choice.strip() for choice in choices.split(',')]

        try:
            result = classifier(query, choices_list)

            return Response({
                'query': query,
                'choices': choices_list,
                'result': result
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)