
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from quiz.models import ClassicQuiz,  EnumQuiz, MatchQuiz
from questions.models import Question
from quiz.serializers import ClassicQuizSerializer, EnumQuizSerializer, MatchQuizSerializer


class AllQuizViewSet(viewsets.ViewSet):
    def list(self, request):
        classic_quizzes = ClassicQuiz.objects.all()
        enum_quizzes = EnumQuiz.objects.all()
        match_quizzes = MatchQuiz.objects.all()

        data = {
            "classic_quizzes": ClassicQuizSerializer(classic_quizzes, many=True).data,
            "enum_quizzes": EnumQuizSerializer(enum_quizzes, many=True).data,
            "match_quizzes": MatchQuizSerializer(match_quizzes, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        # Example: Create a temporary ClassicQuiz with given data
        serializer = ClassicQuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizPickView(APIView):
    def post(self, request, *args, **kwargs):
        # Vérification des données
        data = request.data
        title = data.get("title")
        question_ids = data.get("questions")

        # Vérification des champs requis
        if not title or not question_ids:
            return Response(
                {"error": "Les champs 'title' et 'questions' sont requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vérification du format des questions
        if not isinstance(question_ids, list) or not all(isinstance(q_id, int) for q_id in question_ids):
            return Response(
                {"error": "Le champ 'questions' doit être une liste d'IDs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vérification de l'existence des questions
        questions = Question.objects.filter(id__in=question_ids)
        if questions.count() != len(question_ids):
            return Response(
                {"error": "Certaines questions spécifiées n'existent pas."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Création du quiz
        quiz = ClassicQuiz.objects.create(
            title=title,
            creator=request.user,
            is_temporary_quiz=False,
        )

        # Association des questions
        for idx, question in enumerate(questions):
            quiz.quiz_questions.create(question=question, order=idx)

        # Sérialisation et réponse
        return Response(
            {"quiz_id": quiz.id, "title": quiz.title},
            status=status.HTTP_201_CREATED,
        )
