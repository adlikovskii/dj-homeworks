from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, ArticleScope, Tag


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_main = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            if form.cleaned_data.get('is_main') and form.cleaned_data.get('DELETE') is False:
                count_main += 1
                # вызовом исключения ValidationError можно указать админке о наличие ошибки
                # таким образом объект не будет сохранен,
                # а пользователю выведется соответствующее сообщение об ошибке
        if not count_main:
            raise ValidationError('Выберите основной раздел!')
        elif count_main > 1:
            raise ValidationError('Возможно выбрать только один основной раздел!')
        return super().clean()  # вызываем базовый код переопределяемого метода


class RelationshipInline(admin.TabularInline):
    model = ArticleScope
    extra = 1
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at', 'image']
    inlines = [RelationshipInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
