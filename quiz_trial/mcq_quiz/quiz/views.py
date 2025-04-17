from django.shortcuts import render, redirect
from .models import Quiz, Question, QuizAttempt
from .forms import UserInfoForm
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from datetime import datetime
from .utils import generate_filled_certificate
import os



user_session = {}

def get_active_quiz():
    return Quiz.objects.filter(is_active=True).first()

def user_info_form(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            quiz = get_active_quiz()
            if not quiz:
                return HttpResponse("No active quiz.")
            if QuizAttempt.objects.filter(email=email, quiz=quiz).exists():
                return HttpResponse("You have already attempted this quiz.")
            user_session['name'] = name
            user_session['email'] = email
            return redirect('quiz_view')
    else:
        form = UserInfoForm()
    return render(request, 'quiz/form.html', {'form': form})

def quiz_view(request):
    quiz = get_active_quiz()
    if not quiz:
        return HttpResponse("No active quiz.")
    questions = quiz.questions.all()
    
    return render(request, 'quiz/quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'time_limit': quiz.time_limit
    })

def submit_quiz(request):
    if request.method == 'POST':
        quiz = get_active_quiz()
        if not quiz:
            return HttpResponse("No active quiz.")

        questions = quiz.questions.all()
        score = 0

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected == getattr(question, question.correct_option):
                score += 1


        # Save attempt
        QuizAttempt.objects.create(
            name=user_session['name'],
            email=user_session['email'],
            quiz=quiz,
            score=score
        )
        # Assuming you're inside submit_quiz view
        name = user_session['name']
        email = user_session['email']

        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Quiz: {quiz.title} | ID: {quiz.id}")

        # If disqualified, redirect without generating certificate
        if request.POST.get('disqualified') == '1':
            return redirect('user_info_form')

        #Generate the filled certificate PDF
        name = user_session['name']
        date = datetime.now().strftime("%B %d, %Y")
        request.session['certificate_info'] = {

            'name': name,
            'score': score,
            'date': date
        }


       
        

    return redirect('thank-you')

def thank_you(request):

    cert_info = request.session.get('certificate_info')
    name = cert_info['name']
    score = cert_info['score']
    return render(request, 'quiz/thank_you.html',{
        'name': name, 
        'score': score
    })

def download_certificate(request):
    cert_info = request.session.get('certificate_info')
    if cert_info:
        name = cert_info['name']
        score = cert_info['score']
        date = cert_info['date']

   

    template_path = os.path.join(os.path.dirname(__file__), 'static', 'pdf', 'certificate.png')
    pdf_stream = generate_filled_certificate(name, score, date, template_path)

    response = HttpResponse(pdf_stream, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=certificate_{name}.pdf'
    return response