from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework import generics
from api.serializers import QuestionSerializer, ChoiceSerializer
from polls.models import Question, Choice
from django.utils import timezone
from django.shortcuts import get_object_or_404


class QuestionViewSet(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]

    def create(self, request, *args, **kwargs):
        choices = request.data.get("choices")
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            for choice in choices:
                Choice.objects.create(**choice, question=question)
            serializer = QuestionSerializer(instance=question)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class VoteViewSet(viewsets.ViewSet):
    def create(self, request, pk, format=None):
        queryset = Question.objects.all()
        question = get_object_or_404(queryset, pk=pk)
        try:
            selected_choice = question.choices.get(choice_text=request.data["choice"])
            selected_choice.votes += 1
            selected_choice.save()
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except (KeyError, Choice.DoesNotExist):
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
