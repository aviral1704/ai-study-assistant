"""
Advanced Learning Features for AI Study Assistant
- Progress Tracking
- Personalized Learning Paths
- Spaced Repetition
- Performance Analytics
- Study Recommendations
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import pickle


class LearningTracker:
    """Track student progress and learning patterns."""
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.data_dir = Path(".learning_data")
        self.data_dir.mkdir(exist_ok=True)
        self.data_file = self.data_dir / f"{user_id}_progress.json"
        self.load_progress()
    
    def load_progress(self):
        """Load user progress from file."""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'documents_studied': [],
                'questions_answered': 0,
                'concepts_mastered': [],
                'study_sessions': [],
                'weak_areas': [],
                'strong_areas': [],
                'total_study_time': 0,
                'achievements': [],
                'streak_days': 0,
                'last_study_date': None
            }
    
    def save_progress(self):
        """Save progress to file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def log_study_session(self, document: str, duration: int, topics: List[str]):
        """Log a study session."""
        session = {
            'document': document,
            'duration': duration,
            'topics': topics,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        self.data['study_sessions'].append(session)
        self.data['total_study_time'] += duration
        
        # Update streak
        self._update_streak()
        
        # Check for achievements
        self._check_achievements()
        
        self.save_progress()
    
    def _update_streak(self):
        """Update study streak."""
        today = datetime.now().date()
        last_date = self.data.get('last_study_date')
        
        if last_date:
            last_date = datetime.fromisoformat(last_date).date()
            days_diff = (today - last_date).days
            
            if days_diff == 1:
                self.data['streak_days'] += 1
            elif days_diff > 1:
                self.data['streak_days'] = 1
        else:
            self.data['streak_days'] = 1
        
        self.data['last_study_date'] = today.isoformat()
    
    def _check_achievements(self):
        """Check and award achievements."""
        achievements = []
        
        # Study time achievements
        if self.data['total_study_time'] >= 60 and '1_hour_scholar' not in self.data['achievements']:
            achievements.append('1_hour_scholar')
        if self.data['total_study_time'] >= 600 and '10_hour_master' not in self.data['achievements']:
            achievements.append('10_hour_master')
        
        # Streak achievements
        if self.data['streak_days'] >= 7 and 'week_warrior' not in self.data['achievements']:
            achievements.append('week_warrior')
        if self.data['streak_days'] >= 30 and 'month_champion' not in self.data['achievements']:
            achievements.append('month_champion')
        
        # Question achievements
        if self.data['questions_answered'] >= 50 and 'question_master' not in self.data['achievements']:
            achievements.append('question_master')
        
        self.data['achievements'].extend(achievements)
        return achievements
    
    def get_study_stats(self) -> Dict:
        """Get comprehensive study statistics."""
        return {
            'total_documents': len(self.data['documents_studied']),
            'total_questions': self.data['questions_answered'],
            'total_time': self.data['total_study_time'],
            'streak_days': self.data['streak_days'],
            'concepts_mastered': len(self.data['concepts_mastered']),
            'achievements': len(self.data['achievements']),
            'avg_session_time': self._calculate_avg_session_time(),
            'study_frequency': self._calculate_study_frequency()
        }
    
    def _calculate_avg_session_time(self) -> float:
        """Calculate average study session time."""
        if not self.data['study_sessions']:
            return 0
        total = sum(s['duration'] for s in self.data['study_sessions'])
        return total / len(self.data['study_sessions'])
    
    def _calculate_study_frequency(self) -> str:
        """Calculate how often user studies."""
        if len(self.data['study_sessions']) < 2:
            return "New learner"
        
        sessions = self.data['study_sessions']
        dates = [datetime.fromisoformat(s['timestamp']).date() for s in sessions]
        unique_dates = len(set(dates))
        
        if unique_dates >= 20:
            return "Daily learner"
        elif unique_dates >= 10:
            return "Regular learner"
        else:
            return "Occasional learner"
    
    def get_recommendations(self) -> List[str]:
        """Get personalized study recommendations."""
        recommendations = []
        
        stats = self.get_study_stats()
        
        # Time-based recommendations
        if stats['avg_session_time'] < 15:
            recommendations.append("💡 Try studying for at least 25 minutes per session for better retention")
        
        # Streak recommendations
        if stats['streak_days'] == 0:
            recommendations.append("🔥 Start a study streak! Study every day to build momentum")
        elif stats['streak_days'] < 7:
            recommendations.append(f"🔥 Great! You're on a {stats['streak_days']}-day streak. Keep it going!")
        
        # Weak areas
        if self.data['weak_areas']:
            recommendations.append(f"📚 Focus on: {', '.join(self.data['weak_areas'][:3])}")
        
        # Practice recommendations
        if stats['total_questions'] < 20:
            recommendations.append("🎯 Practice more questions to test your understanding")
        
        return recommendations


class SpacedRepetition:
    """Implement spaced repetition for optimal learning."""
    
    def __init__(self):
        self.cards = {}
        self.data_file = Path(".learning_data/spaced_repetition.pkl")
        self.load_cards()
    
    def load_cards(self):
        """Load flashcards from file."""
        if self.data_file.exists():
            with open(self.data_file, 'rb') as f:
                self.cards = pickle.load(f)
    
    def save_cards(self):
        """Save flashcards to file."""
        self.data_file.parent.mkdir(exist_ok=True)
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.cards, f)
    
    def add_card(self, concept: str, definition: str):
        """Add a new flashcard."""
        self.cards[concept] = {
            'definition': definition,
            'interval': 1,  # days
            'ease_factor': 2.5,
            'repetitions': 0,
            'next_review': datetime.now(),
            'last_reviewed': None
        }
        self.save_cards()
    
    def review_card(self, concept: str, quality: int):
        """
        Review a card and update its schedule.
        quality: 0-5 (0=complete blackout, 5=perfect response)
        """
        if concept not in self.cards:
            return
        
        card = self.cards[concept]
        
        if quality < 3:
            # Reset if answer was poor
            card['repetitions'] = 0
            card['interval'] = 1
        else:
            if card['repetitions'] == 0:
                card['interval'] = 1
            elif card['repetitions'] == 1:
                card['interval'] = 6
            else:
                card['interval'] = round(card['interval'] * card['ease_factor'])
            
            card['repetitions'] += 1
            card['ease_factor'] = max(1.3, card['ease_factor'] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        card['last_reviewed'] = datetime.now()
        card['next_review'] = datetime.now() + timedelta(days=card['interval'])
        
        self.save_cards()
    
    def get_due_cards(self) -> List[Dict]:
        """Get cards that are due for review."""
        now = datetime.now()
        due_cards = []
        
        for concept, card in self.cards.items():
            if card['next_review'] <= now:
                due_cards.append({
                    'concept': concept,
                    'definition': card['definition'],
                    'repetitions': card['repetitions']
                })
        
        return due_cards
    
    def get_stats(self) -> Dict:
        """Get spaced repetition statistics."""
        total = len(self.cards)
        due = len(self.get_due_cards())
        mastered = sum(1 for c in self.cards.values() if c['repetitions'] >= 5)
        
        return {
            'total_cards': total,
            'due_today': due,
            'mastered': mastered,
            'learning': total - mastered
        }


class StudyPlanner:
    """Create personalized study plans."""
    
    def __init__(self, tracker: LearningTracker):
        self.tracker = tracker
    
    def create_study_plan(self, exam_date: datetime, topics: List[str], hours_per_day: int = 2) -> Dict:
        """Create a personalized study plan."""
        days_until_exam = (exam_date - datetime.now()).days
        
        if days_until_exam <= 0:
            return {"error": "Exam date must be in the future"}
        
        total_hours = days_until_exam * hours_per_day
        hours_per_topic = total_hours / len(topics)
        
        plan = {
            'exam_date': exam_date.strftime('%Y-%m-%d'),
            'days_remaining': days_until_exam,
            'total_study_hours': total_hours,
            'daily_schedule': [],
            'topic_allocation': {}
        }
        
        # Allocate time per topic
        for topic in topics:
            plan['topic_allocation'][topic] = {
                'hours': round(hours_per_topic, 1),
                'sessions': round(hours_per_topic / hours_per_day)
            }
        
        # Create daily schedule
        current_date = datetime.now()
        topic_index = 0
        
        for day in range(days_until_exam):
            date = current_date + timedelta(days=day)
            topic = topics[topic_index % len(topics)]
            
            plan['daily_schedule'].append({
                'date': date.strftime('%Y-%m-%d'),
                'day_name': date.strftime('%A'),
                'topic': topic,
                'duration': hours_per_day,
                'tasks': [
                    f"Review {topic} concepts",
                    f"Practice {topic} questions",
                    f"Summarize key points"
                ]
            })
            
            topic_index += 1
        
        # Add review days
        review_days = [days_until_exam - 7, days_until_exam - 3, days_until_exam - 1]
        for review_day in review_days:
            if 0 <= review_day < len(plan['daily_schedule']):
                plan['daily_schedule'][review_day]['tasks'] = [
                    "📚 REVIEW DAY - Review all topics",
                    "🎯 Take practice exam",
                    "📝 Review weak areas"
                ]
        
        return plan
    
    def get_daily_tasks(self) -> List[str]:
        """Get recommended tasks for today."""
        stats = self.tracker.get_study_stats()
        
        tasks = [
            "📖 Study for at least 25 minutes",
            "🎯 Answer 10 practice questions",
            "📝 Review yesterday's notes"
        ]
        
        if stats['streak_days'] > 0:
            tasks.append(f"🔥 Maintain your {stats['streak_days']}-day streak!")
        
        return tasks


def get_achievement_badge(achievement: str) -> str:
    """Get emoji badge for achievement."""
    badges = {
        '1_hour_scholar': '⏰ 1-Hour Scholar',
        '10_hour_master': '🎓 10-Hour Master',
        'week_warrior': '🔥 Week Warrior',
        'month_champion': '👑 Month Champion',
        'question_master': '🎯 Question Master',
        'speed_reader': '⚡ Speed Reader',
        'perfect_score': '💯 Perfect Score',
        'early_bird': '🌅 Early Bird',
        'night_owl': '🦉 Night Owl'
    }
    return badges.get(achievement, '🏆 Achievement Unlocked')
