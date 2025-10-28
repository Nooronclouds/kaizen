"""
Learning curriculum and roadmaps for different programming languages.

Provides predefined topic sequences with difficulty ratings for the adaptive scheduler.
"""

from typing import List, Dict


class Topic:
    """
    Represents a single learning topic in the curriculum.

    Attributes:
        name: Topic name (e.g., "Variables", "Functions")
        difficulty: Difficulty rating from 0.0 (easy) to 1.0 (hard)
        estimated_days: Typical days needed to master this topic
    """
    def __init__(self, name: str, difficulty: float, estimated_days: int = 1):
        self.name = name
        self.difficulty = difficulty
        self.estimated_days = estimated_days

    def to_dict(self) -> dict:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "difficulty": self.difficulty,
            "estimated_days": self.estimated_days
        }


# Python Programming Curriculum
PYTHON_CURRICULUM = [
    Topic("Variables and Data Types", 0.2, 1),
    Topic("Basic Operators", 0.2, 1),
    Topic("String Operations", 0.3, 1),
    Topic("Lists and Indexing", 0.4, 2),
    Topic("Conditional Statements", 0.4, 1),
    Topic("Loops (for and while)", 0.5, 2),
    Topic("Functions", 0.5, 2),
    Topic("Dictionaries", 0.5, 2),
    Topic("List Comprehensions", 0.6, 1),
    Topic("Tuples and Sets", 0.5, 1),
    Topic("File I/O", 0.6, 2),
    Topic("Exception Handling", 0.6, 2),
    Topic("Modules and Imports", 0.5, 1),
    Topic("Object-Oriented Programming Basics", 0.7, 3),
    Topic("Classes and Objects", 0.7, 2),
    Topic("Inheritance", 0.7, 2),
    Topic("Decorators", 0.8, 2),
    Topic("Generators and Iterators", 0.8, 2),
    Topic("Lambda Functions", 0.6, 1),
    Topic("Working with JSON", 0.6, 1),
]

# JavaScript Curriculum
JAVASCRIPT_CURRICULUM = [
    Topic("Variables (let, const, var)", 0.2, 1),
    Topic("Data Types", 0.2, 1),
    Topic("Operators", 0.2, 1),
    Topic("Strings and Template Literals", 0.3, 1),
    Topic("Arrays", 0.4, 2),
    Topic("Conditional Statements", 0.4, 1),
    Topic("Loops", 0.5, 2),
    Topic("Functions", 0.5, 2),
    Topic("Arrow Functions", 0.5, 1),
    Topic("Objects", 0.5, 2),
    Topic("Array Methods (map, filter, reduce)", 0.6, 2),
    Topic("Destructuring", 0.6, 1),
    Topic("Spread and Rest Operators", 0.6, 1),
    Topic("DOM Manipulation", 0.6, 2),
    Topic("Events and Event Listeners", 0.6, 2),
    Topic("Promises", 0.7, 2),
    Topic("Async/Await", 0.7, 2),
    Topic("Classes and OOP", 0.7, 2),
    Topic("Modules (import/export)", 0.6, 1),
    Topic("Error Handling", 0.6, 1),
]

# Java Curriculum
JAVA_CURRICULUM = [
    Topic("Variables and Data Types", 0.3, 1),
    Topic("Operators", 0.3, 1),
    Topic("Strings", 0.3, 1),
    Topic("Arrays", 0.4, 2),
    Topic("Conditional Statements", 0.4, 1),
    Topic("Loops", 0.5, 2),
    Topic("Methods", 0.5, 2),
    Topic("Object-Oriented Programming Basics", 0.6, 3),
    Topic("Classes and Objects", 0.6, 2),
    Topic("Constructors", 0.6, 1),
    Topic("Inheritance", 0.7, 2),
    Topic("Polymorphism", 0.7, 2),
    Topic("Interfaces", 0.7, 2),
    Topic("Abstract Classes", 0.7, 2),
    Topic("Exception Handling", 0.6, 2),
    Topic("Collections Framework", 0.7, 3),
    Topic("ArrayList and LinkedList", 0.6, 2),
    Topic("HashMap and HashSet", 0.7, 2),
    Topic("File I/O", 0.6, 2),
    Topic("Generics", 0.8, 2),
]

# Curriculum mapping
CURRICULUMS: Dict[str, List[Topic]] = {
    "python": PYTHON_CURRICULUM,
    "javascript": JAVASCRIPT_CURRICULUM,
    "java": JAVA_CURRICULUM,
}


def get_curriculum(language: str) -> List[Topic]:
    """
    Get the curriculum for a specific programming language.

    Args:
        language: Programming language name (lowercase)

    Returns:
        List of Topic objects representing the learning path

    Raises:
        ValueError: If language is not supported
    """
    language = language.lower()

    if language not in CURRICULUMS:
        supported = ", ".join(CURRICULUMS.keys())
        raise ValueError(f"Language '{language}' not supported. Supported languages: {supported}")

    return CURRICULUMS[language]


def get_topic_by_name(language: str, topic_name: str) -> Topic:
    """
    Get a specific topic from a curriculum by name.

    Args:
        language: Programming language name
        topic_name: Name of the topic to find

    Returns:
        Topic object if found

    Raises:
        ValueError: If language not supported or topic not found
    """
    curriculum = get_curriculum(language)

    for topic in curriculum:
        if topic.name.lower() == topic_name.lower():
            return topic

    raise ValueError(f"Topic '{topic_name}' not found in {language} curriculum")


def get_curriculum_length(language: str) -> int:
    """
    Get the total number of topics in a curriculum.

    Args:
        language: Programming language name

    Returns:
        Number of topics in the curriculum
    """
    curriculum = get_curriculum(language)
    return len(curriculum)


def get_supported_languages() -> List[str]:
    """
    Get list of all supported programming languages.

    Returns:
        List of supported language names
    """
    return list(CURRICULUMS.keys())
