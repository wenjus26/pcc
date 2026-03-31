from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evaluation, Question, Choice, UserResult, Badge
from apps.citizens.models import CitizenProfile

@login_required
def evaluation_list(request):
    """Lists all available evaluations for the user."""
    evaluations = Evaluation.objects.filter(is_active=True)
    
    # Get or create profile safely
    profile, _ = CitizenProfile.objects.get_or_create(user=request.user)
    user_results = UserResult.objects.filter(profile=profile)
    
    # Create a map of evaluations passed by the user
    passed_evals = {result.evaluation_id: result for result in user_results}
    
    context = {
        'evaluations': evaluations,
        'passed_evals': passed_evals,
    }
    return render(request, 'evaluations/evaluation_list.html', context)

@login_required
def take_evaluation(request, uuid):
    """Interface to take a specific evaluation."""
    evaluation = get_object_or_404(Evaluation, uuid=uuid, is_active=True)
    
    if request.method == 'POST':
        # Simple scoring logic
        questions = evaluation.questions.all()
        total_questions = questions.count()
        correct_answers = 0
        
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            if choice_id:
                try:
                    choice = Choice.objects.get(id=choice_id, question=question)
                    if choice.is_correct:
                        correct_answers += 1
                except Choice.DoesNotExist:
                    pass
        
        score_percent = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        passed = score_percent >= evaluation.passing_score
        
        # Save result
        profile, _ = CitizenProfile.objects.get_or_create(user=request.user)
        result = UserResult.objects.create(
            profile=profile,
            evaluation=evaluation,
            score=score_percent,
            passed=passed
        )
        
        if passed:
            messages.success(request, f"Félicitations ! Vous avez réussi l'évaluation '{evaluation.title}' avec un score de {score_percent:.1f}%.")
        else:
            messages.warning(request, f"Vous n'avez pas atteint le score requis pour '{evaluation.title}'. Votre score : {score_percent:.1f}%.")
            
        return redirect('evaluations:evaluation_result', pk=result.pk)

    return render(request, 'evaluations/take_evaluation.html', {'evaluation': evaluation})

@login_required
def evaluation_result(request, pk):
    """Displays the result of an evaluation."""
    profile, _ = CitizenProfile.objects.get_or_create(user=request.user)
    result = get_object_or_404(UserResult, pk=pk, profile=profile)
    return render(request, 'evaluations/evaluation_result.html', {'result': result})
