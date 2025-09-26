"""
Formatters for data formatting and presentation
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import json

class DataFormatter:
    """Base class for data formatting"""
    
    @staticmethod
    def format_percentage(value: float, decimal_places: int = 2) -> str:
        """Format percentage with specified decimal places"""
        return f"{value:.{decimal_places}f}%"
    
    @staticmethod
    def format_number(value: float, decimal_places: int = 2) -> str:
        """Format number with specified decimal places"""
        return f"{value:.{decimal_places}f}"
    
    @staticmethod
    def format_currency(value: float, currency: str = "$") -> str:
        """Format currency value"""
        return f"{currency}{value:.2f}"
    
    @staticmethod
    def format_list(items: List[Any], separator: str = ", ") -> str:
        """Format list as string"""
        return separator.join(str(item) for item in items)
    
    @staticmethod
    def format_dict(data: Dict[str, Any], indent: int = 2) -> str:
        """Format dictionary as formatted string"""
        return json.dumps(data, indent=indent, default=str)

class DateFormatter:
    """Date and time formatting utilities"""
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime object"""
        if not dt:
            return "N/A"
        return dt.strftime(format_str)
    
    @staticmethod
    def format_date(dt: datetime, format_str: str = "%Y-%m-%d") -> str:
        """Format date only"""
        if not dt:
            return "N/A"
        return dt.strftime(format_str)
    
    @staticmethod
    def format_time(dt: datetime, format_str: str = "%H:%M:%S") -> str:
        """Format time only"""
        if not dt:
            return "N/A"
        return dt.strftime(format_str)
    
    @staticmethod
    def format_relative_time(dt: datetime) -> str:
        """Format relative time (e.g., '2 hours ago')"""
        if not dt:
            return "N/A"
        
        now = datetime.utcnow()
        diff = now - dt
        
        if diff.days > 0:
            if diff.days == 1:
                return "1 day ago"
            return f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            if hours == 1:
                return "1 hour ago"
            return f"{hours} hours ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            if minutes == 1:
                return "1 minute ago"
            return f"{minutes} minutes ago"
        else:
            return "Just now"
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """Format duration in seconds to human readable format"""
        if seconds < 60:
            return f"{seconds} seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes} minutes"
            return f"{minutes} minutes {remaining_seconds} seconds"
        else:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            if remaining_minutes == 0:
                return f"{hours} hours"
            return f"{hours} hours {remaining_minutes} minutes"

class ScoreFormatter:
    """Score and grade formatting utilities"""
    
    @staticmethod
    def format_score(score: int, total: int) -> str:
        """Format score as fraction"""
        return f"{score}/{total}"
    
    @staticmethod
    def format_percentage_score(score: int, total: int, decimal_places: int = 1) -> str:
        """Format score as percentage"""
        if total == 0:
            return "0%"
        percentage = (score / total) * 100
        return f"{percentage:.{decimal_places}f}%"
    
    @staticmethod
    def get_grade(percentage: float) -> str:
        """Get letter grade based on percentage"""
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"
    
    @staticmethod
    def get_grade_with_plus_minus(percentage: float) -> str:
        """Get letter grade with plus/minus based on percentage"""
        if percentage >= 97:
            return "A+"
        elif percentage >= 93:
            return "A"
        elif percentage >= 90:
            return "A-"
        elif percentage >= 87:
            return "B+"
        elif percentage >= 83:
            return "B"
        elif percentage >= 80:
            return "B-"
        elif percentage >= 77:
            return "C+"
        elif percentage >= 73:
            return "C"
        elif percentage >= 70:
            return "C-"
        elif percentage >= 67:
            return "D+"
        elif percentage >= 63:
            return "D"
        elif percentage >= 60:
            return "D-"
        else:
            return "F"
    
    @staticmethod
    def get_performance_level(percentage: float) -> str:
        """Get performance level description"""
        if percentage >= 90:
            return "Excellent"
        elif percentage >= 80:
            return "Good"
        elif percentage >= 70:
            return "Average"
        elif percentage >= 60:
            return "Below Average"
        else:
            return "Needs Improvement"
    
    @staticmethod
    def format_score_with_grade(score: int, total: int) -> Dict[str, str]:
        """Format score with all grade information"""
        percentage = (score / total) * 100 if total > 0 else 0
        
        return {
            'score': ScoreFormatter.format_score(score, total),
            'percentage': ScoreFormatter.format_percentage_score(score, total),
            'grade': ScoreFormatter.get_grade(percentage),
            'grade_detailed': ScoreFormatter.get_grade_with_plus_minus(percentage),
            'performance_level': ScoreFormatter.get_performance_level(percentage)
        }

class ProgressFormatter:
    """Progress formatting utilities"""
    
    @staticmethod
    def format_progress_bar(current: int, total: int, width: int = 20) -> str:
        """Format progress as ASCII progress bar"""
        if total == 0:
            return "[" + " " * width + "] 0%"
        
        percentage = (current / total) * 100
        filled_width = int((current / total) * width)
        
        bar = "█" * filled_width + "░" * (width - filled_width)
        return f"[{bar}] {percentage:.1f}%"
    
    @staticmethod
    def format_completion_status(completed: int, total: int) -> str:
        """Format completion status"""
        if total == 0:
            return "No items"
        
        if completed == total:
            return "Completed"
        elif completed == 0:
            return "Not started"
        else:
            return f"{completed} of {total} completed"
    
    @staticmethod
    def format_time_spent(minutes: int) -> str:
        """Format time spent in human readable format"""
        if minutes < 60:
            return f"{minutes} minutes"
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if remaining_minutes == 0:
                return f"{hours} hours"
            return f"{hours} hours {remaining_minutes} minutes"

class TextFormatter:
    """Text formatting utilities"""
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def capitalize_words(text: str) -> str:
        """Capitalize first letter of each word"""
        return text.title()
    
    @staticmethod
    def format_name(first_name: str, last_name: str) -> str:
        """Format full name properly"""
        return f"{first_name.capitalize()} {last_name.capitalize()}"
    
    @staticmethod
    def format_username(username: str) -> str:
        """Format username for display"""
        return f"@{username}"
    
    @staticmethod
    def format_list_with_numbers(items: List[str]) -> str:
        """Format list with numbers"""
        if not items:
            return ""
        
        formatted_items = []
        for i, item in enumerate(items, 1):
            formatted_items.append(f"{i}. {item}")
        
        return "\n".join(formatted_items)
    
    @staticmethod
    def format_bullet_list(items: List[str], bullet: str = "•") -> str:
        """Format list with bullets"""
        if not items:
            return ""
        
        formatted_items = []
        for item in items:
            formatted_items.append(f"{bullet} {item}")
        
        return "\n".join(formatted_items)

class JSONFormatter:
    """JSON formatting utilities"""
    
    @staticmethod
    def format_json(data: Any, indent: int = 2) -> str:
        """Format data as JSON string"""
        return json.dumps(data, indent=indent, default=str)
    
    @staticmethod
    def format_json_compact(data: Any) -> str:
        """Format data as compact JSON string"""
        return json.dumps(data, separators=(',', ':'), default=str)
    
    @staticmethod
    def parse_json(json_string: str) -> Any:
        """Parse JSON string to Python object"""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            return None
    
    @staticmethod
    def is_valid_json(json_string: str) -> bool:
        """Check if string is valid JSON"""
        try:
            json.loads(json_string)
            return True
        except json.JSONDecodeError:
            return False

