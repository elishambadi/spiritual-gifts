from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django.utils import timezone
from .models import SpiritualGift, Question, SurveyResponse, Answer
from .serializers import (
    SpiritualGiftSerializer, 
    QuestionSerializer, 
    SurveyResponseSerializer,
    SurveyResultSerializer
)


class SpiritualGiftViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for spiritual gifts."""
    queryset = SpiritualGift.objects.all()
    serializer_class = SpiritualGiftSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for survey questions."""
    queryset = Question.objects.all().select_related('spiritual_gift')
    serializer_class = QuestionSerializer


class SurveyResponseViewSet(viewsets.ModelViewSet):
    """API endpoint for survey responses."""
    queryset = SurveyResponse.objects.all().prefetch_related('answers')
    serializer_class = SurveyResponseSerializer
    lookup_field = 'id'
    
    @action(detail=True, methods=['patch'])
    def update_answers(self, request, id=None):
        """Update answers for a survey response."""
        survey_response = self.get_object()
        answers_data = request.data.get('answers', [])
        
        for answer_data in answers_data:
            question_id = answer_data.get('question')
            rating = answer_data.get('rating')
            
            Answer.objects.update_or_create(
                survey_response=survey_response,
                question_id=question_id,
                defaults={'rating': rating}
            )
        
        serializer = self.get_serializer(survey_response)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def results(self, request, id=None):
        """Get calculated results for a survey response."""
        survey_response = self.get_object()
        gift_scores = survey_response.calculate_results()
        
        # Calculate total and percentage
        total_score = sum(score for _, score in gift_scores)
        
        results = []
        for gift_name, score in gift_scores:
            percentage = (score / total_score * 100) if total_score > 0 else 0
            results.append({
                'gift_name': gift_name,
                'score': score,
                'percentage': round(percentage, 2)
            })
        
        serializer = SurveyResultSerializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, id=None):
        """Mark a survey response as completed."""
        survey_response = self.get_object()
        survey_response.completed_at = timezone.now()
        survey_response.is_complete = True
        survey_response.save()
        
        serializer = self.get_serializer(survey_response)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def admin_leaderboard(self, request):
        """Admin-only leaderboard: top 5 performers by percentage for each gift."""
        responses = SurveyResponse.objects.filter(is_complete=True).prefetch_related(
            'answers__question__spiritual_gift'
        )
        gifts = SpiritualGift.objects.all()

        gift_performers = {gift.name: [] for gift in gifts}

        for response in responses:
            gift_scores = {}
            total_score = 0

            for answer in response.answers.all():
                gift_name = answer.question.spiritual_gift.name
                gift_scores[gift_name] = gift_scores.get(gift_name, 0) + answer.rating
                total_score += answer.rating

            if total_score == 0:
                continue

            for gift_name, score in gift_scores.items():
                percentage = round((score / total_score) * 100, 2)
                gift_performers[gift_name].append({
                    'response_id': str(response.id),
                    'name': response.name or 'Anonymous',
                    'percentage': percentage,
                    'score': score
                })

        leaderboard = []
        for gift in gifts:
            performers = sorted(
                gift_performers[gift.name],
                key=lambda item: item['percentage'],
                reverse=True
            )[:5]
            leaderboard.append({
                'gift_name': gift.name,
                'top_performers': performers
            })

        return Response(leaderboard)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def public_summaries(self, request):
        """Public summaries: top 3 gift names for each completed response."""
        responses = SurveyResponse.objects.filter(is_complete=True).prefetch_related(
            'answers__question__spiritual_gift'
        )

        summaries = []
        for response in responses:
            gift_scores = {}
            for answer in response.answers.all():
                gift_name = answer.question.spiritual_gift.name
                gift_scores[gift_name] = gift_scores.get(gift_name, 0) + answer.rating

            top_gifts = [
                gift_name for gift_name, _ in sorted(
                    gift_scores.items(), key=lambda item: item[1], reverse=True
                )[:3]
            ]

            summaries.append({
                'response_id': str(response.id),
                'name': response.name or 'Anonymous',
                'top_gifts': top_gifts
            })

        return Response(summaries)
