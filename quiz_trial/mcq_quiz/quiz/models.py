from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes")
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    
    OPTION_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
    ]
    correct_option = models.CharField(max_length=10, choices=OPTION_CHOICES)

    def __str__(self):
        return self.question_text

class QuizAttempt(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.quiz.title} - {self.score}"
