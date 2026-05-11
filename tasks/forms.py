from django import forms
from .models import Task
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    """Admin-facing task form with workflow and assignee controls."""

    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Assign To"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Present usernames in a more readable label format in the checkbox list.
        self.fields['assigned_to'].label_from_instance = lambda user: user.username.capitalize()

    class Meta:
        model = Task
        fields = ['title', 'description', 'note', 'due_date', 'assigned_to', 'priority', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control focusflow-input', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control focusflow-textarea', 'rows': 4, 'placeholder': 'Add a short task description'}),
            'note': forms.Textarea(attrs={'class': 'form-control focusflow-textarea', 'rows': 3, 'placeholder': 'Optional internal note'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control focusflow-input'}),
            'priority': forms.Select(attrs={'class': 'form-select focusflow-select'}),
            'status': forms.Select(attrs={'class': 'form-select focusflow-select'}),
        }
