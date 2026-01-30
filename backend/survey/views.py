from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
