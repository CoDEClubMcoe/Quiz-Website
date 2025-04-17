from django.contrib import admin
from .models import Quiz, Question, QuizAttempt
from django.db.models import Max

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ('question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    inlines = [QuestionInline]
    actions = ['make_active']

    def make_active(self, request, queryset):
        Quiz.objects.update(is_active=False)
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected quiz as active"



class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'quiz', 'score', 'timestamp')
    readonly_fields = ('name', 'email', 'quiz', 'score', 'timestamp')
    search_fields = ('name', 'email')
    ordering = ('quiz', 'email')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Get the latest timestamp for each email + quiz combo
        latest_attempts = QuizAttempt.objects.values('email', 'quiz').annotate(
            latest_timestamp=Max('timestamp')
        )

        # Now get only those attempts that match these latest timestamps
        filters = [
            {'email': item['email'], 'quiz': item['quiz'], 'timestamp': item['latest_timestamp']}
            for item in latest_attempts
        ]

        # Manually build a queryset that contains only the latest attempts
        from django.db.models import Q
        final_qs = QuizAttempt.objects.none()
        for f in filters:
            final_qs |= qs.filter(**f)

        return final_qs


admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizAttempt, QuizAttemptAdmin)
