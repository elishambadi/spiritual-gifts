from django.core.management.base import BaseCommand
from django.conf import settings
from survey.models import SpiritualGift, Question
import os
import re


class Command(BaseCommand):
    help = 'Populate the database with spiritual gifts and survey questions from questions.md'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating spiritual gifts and questions from questions.md...')
        
        # Find questions.md in the project root (one level up from backend/)
        base_dir = settings.BASE_DIR.parent  # This gets us to the project root
        questions_file = os.path.join(base_dir, 'questions.md')
        
        if not os.path.exists(questions_file):
            self.stdout.write(self.style.ERROR(f'questions.md not found at {questions_file}'))
            return
        
        with open(questions_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Define spiritual gifts with descriptions based on the scoring section
        gifts_data = {
            'Leadership': 'The gift of setting goals and motivating people to accomplish these goals.',
            'Administration': 'The gift of organizing ideas, resources, time, and people effectively.',
            'Teaching': 'The gift of communicating information relevant to spiritual growth and health.',
            'Knowledge': 'The gift of discovering, accumulating, and clarifying information and ideas.',
            'Wisdom': 'The gift of applying knowledge to practical situations with insight.',
            'Prophecy': 'The gift of proclaiming the Word of God boldly and speaking truth to the church.',
            'Discernment': 'The gift of distinguishing between truth and error, good and evil spirits.',
            'Exhortation': 'The gift of encouraging, comforting, and urging people to action.',
            'Shepherding': 'The gift of caring for the spiritual needs of a group of believers.',
            'Faith': 'The gift of acting on God\'s promises with confidence and trust.',
            'Evangelism': 'The gift of presenting the gospel to unbelievers in a clear and meaningful way.',
            'Apostleship': 'The gift of starting and overseeing new churches and ministries.',
            'Service/Helps': 'The gift of identifying unmet needs and taking initiative to meet those needs.',
            'Mercy': 'The gift of feeling and expressing compassion for those who are hurting.',
            'Giving': 'The gift of contributing material resources with generosity and cheerfulness.',
            'Hospitality': 'The gift of making others feel welcome and comfortable.'
        }
        
        # Create spiritual gifts
        gifts = {}
        for name, description in gifts_data.items():
            gift, created = SpiritualGift.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            gifts[name] = gift
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created gift: {name}'))
        
        # Parse questions from the markdown file
        # Pattern to match: ______ 1. Question text goes here.
        question_pattern = r'______\s+(\d+)\.\s+(.+?)(?=\n______|\nSCORING YOUR SURVEY|$)'
        matches = re.findall(question_pattern, content, re.DOTALL)
        
        # Map questions to gifts based on the scoring section
        gift_mapping = {
            # Leadership: 6, 16, 27, 43, 65
            6: 'Leadership', 16: 'Leadership', 27: 'Leadership', 43: 'Leadership', 65: 'Leadership',
            # Administration: 1, 17, 31, 47, 59
            1: 'Administration', 17: 'Administration', 31: 'Administration', 47: 'Administration', 59: 'Administration',
            # Teaching: 2, 18, 33, 61, 73
            2: 'Teaching', 18: 'Teaching', 33: 'Teaching', 61: 'Teaching', 73: 'Teaching',
            # Knowledge: 9, 24, 39, 68, 79
            9: 'Knowledge', 24: 'Knowledge', 39: 'Knowledge', 68: 'Knowledge', 79: 'Knowledge',
            # Wisdom: 3, 19, 48, 62, 74
            3: 'Wisdom', 19: 'Wisdom', 48: 'Wisdom', 62: 'Wisdom', 74: 'Wisdom',
            # Prophecy: 10, 25, 40, 54, 69
            10: 'Prophecy', 25: 'Prophecy', 40: 'Prophecy', 54: 'Prophecy', 69: 'Prophecy',
            # Discernment: 11, 26, 41, 55, 70
            11: 'Discernment', 26: 'Discernment', 41: 'Discernment', 55: 'Discernment', 70: 'Discernment',
            # Exhortation: 20, 34, 49, 63, 75
            20: 'Exhortation', 34: 'Exhortation', 49: 'Exhortation', 63: 'Exhortation', 75: 'Exhortation',
            # Shepherding: 4, 21, 35, 50, 76
            4: 'Shepherding', 21: 'Shepherding', 35: 'Shepherding', 50: 'Shepherding', 76: 'Shepherding',
            # Faith: 12, 28, 42, 56, 80
            12: 'Faith', 28: 'Faith', 42: 'Faith', 56: 'Faith', 80: 'Faith',
            # Evangelism: 5, 36, 51, 64, 77
            5: 'Evangelism', 36: 'Evangelism', 51: 'Evangelism', 64: 'Evangelism', 77: 'Evangelism',
            # Apostleship: 13, 29, 44, 57, 71
            13: 'Apostleship', 29: 'Apostleship', 44: 'Apostleship', 57: 'Apostleship', 71: 'Apostleship',
            # Service/Helps: 14, 30, 46, 58, 72
            14: 'Service/Helps', 30: 'Service/Helps', 46: 'Service/Helps', 58: 'Service/Helps', 72: 'Service/Helps',
            # Mercy: 7, 22, 37, 52, 66
            7: 'Mercy', 22: 'Mercy', 37: 'Mercy', 52: 'Mercy', 66: 'Mercy',
            # Giving: 8, 23, 38, 53, 67
            8: 'Giving', 23: 'Giving', 38: 'Giving', 53: 'Giving', 67: 'Giving',
            # Hospitality: 15, 32, 45, 60, 78
            15: 'Hospitality', 32: 'Hospitality', 45: 'Hospitality', 60: 'Hospitality', 78: 'Hospitality',
        }
        
        questions_created = 0
        for number_str, text in matches:
            number = int(number_str)
            # Clean up the question text
            text = text.strip().replace('\n', ' ').replace('  ', ' ')
            
            # Get the gift for this question
            gift_name = gift_mapping.get(number)
            if not gift_name:
                self.stdout.write(self.style.WARNING(f'No gift mapping for question {number}'))
                continue
            
            # Create the question
            question, created = Question.objects.get_or_create(
                number=number,
                defaults={
                    'text': text,
                    'spiritual_gift': gifts[gift_name]
                }
            )
            if created:
                questions_created += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {len(gifts_data)} spiritual gifts and {questions_created} questions'
        ))
