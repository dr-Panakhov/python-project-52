import django_filters
from django import forms
from .models import Task
from labels.models import Label

class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка'
    )
    self_task = django_filters.BooleanFilter(
        label='Только свои задачи',
        widget=forms.CheckboxInput(),
        method='filter_self',
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_self(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
