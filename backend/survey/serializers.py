from rest_framework import serializers
from .models import SpiritualGift, Question, SurveyResponse, Answer


class SpiritualGiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpiritualGift
        fields = ['id', 'name', 'description']


class QuestionSerializer(serializers.ModelSerializer):
    spiritual_gift_name = serializers.CharField(source='spiritual_gift.name', read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'number', 'text', 'spiritual_gift', 'spiritual_gift_name']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'rating']


class SurveyResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, required=False)
    
    class Meta:
        model = SurveyResponse
        fields = ['id', 'name', 'email', 'created_at', 'completed_at', 'is_complete', 'answers']
        read_only_fields = ['created_at', 'id']
    
    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        survey_response = SurveyResponse.objects.create(**validated_data)
        
        for answer_data in answers_data:
            Answer.objects.create(survey_response=survey_response, **answer_data)
        
        return survey_response


class SurveyResultSerializer(serializers.Serializer):
    """Serializer for survey results/scores."""
    gift_name = serializers.CharField()
    score = serializers.IntegerField()
    percentage = serializers.FloatField()
