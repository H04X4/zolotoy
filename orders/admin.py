from django.contrib import admin
from .models import Product, UserProfile
import pandas as pd
from django import forms
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label="Файл Excel", help_text="Выберите файл в формате .xls или .xlsx")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['article', 'stock', 'store_presence', 'cost_price', 'order_quantity', 'comment', 'unique_number']
    change_list_template = 'admin/product_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.upload_excel, name='upload_excel'),
        ]
        return custom_urls + urls

    def upload_excel(self, request):
        if request.method == 'POST':
            form = ExcelUploadForm(request.POST, request.FILES)
            if not request.FILES.get('excel_file'):
                messages.error(request, "Файл не выбран. Пожалуйста, выберите файл Excel.")
                return render(request, 'admin/upload_excel.html', {'form': form})

            if form.is_valid():
                excel_file = request.FILES['excel_file']
                if not excel_file.name.lower().endswith(('.xls', '.xlsx')):
                    messages.error(request, "Неверный формат файла. Используйте .xls или .xlsx.")
                    return render(request, 'admin/upload_excel.html', {'form': form})

                try:
                    df = pd.read_excel(excel_file)
                    required_columns = ['article', 'stock', 'store_presence', 'cost_price']
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    if missing_columns:
                        messages.error(request, f"Отсутствуют обязательные столбцы: {', '.join(missing_columns)}")
                        return render(request, 'admin/upload_excel.html', {'form': form})

                    created_count = 0
                    updated_count = 0
                    errors = []
                    for index, row in df.iterrows():
                        try:
                            article = str(row['article']).strip()
                            if not article:
                                errors.append(f"Пустой артикул в строке {index + 2}")
                                continue
                            defaults = {
                                'image': str(row.get('image', '')),
                                'stock': int(row['stock']),
                                'store_presence': str(row.get('store_presence', '')),
                                'cost_price': float(row['cost_price']),
                                'order_quantity': int(row.get('order_quantity', 0)),
                                'comment': str(row.get('comment', '')),
                                'unique_number': int(row['unique_number']) if pd.notna(row.get('unique_number')) else None,
                            }
                            product, created = Product.objects.update_or_create(
                                article=article,
                                defaults=defaults
                            )
                            if created:
                                created_count += 1
                            else:
                                updated_count += 1
                        except Exception as e:
                            errors.append(f"Ошибка в строке {index + 2}: {str(e)}")
                            continue

                    if errors:
                        messages.warning(request, f"Обработано с ошибками: {', '.join(errors)}")
                    messages.success(request, f"Файл Excel обработан: {created_count} записей создано, {updated_count} обновлено.")
                    total_records = Product.objects.count()
                    messages.info(request, f"Всего записей в базе после загрузки: {total_records}")
                    return HttpResponseRedirect('../')
                except Exception as e:
                    messages.error(request, f"Ошибка при обработке файла: {str(e)}")
                    return render(request, 'admin/upload_excel.html', {'form': form})
            else:
                messages.error(request, f"Форма недействительна: {form.errors.as_text()}")
                return render(request, 'admin/upload_excel.html', {'form': form})
        form = ExcelUploadForm()
        return render(request, 'admin/upload_excel.html', {'form': form})

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_staff', 'get_unique_number')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'profile__unique_number')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Дополнительно', {'fields': ('profile',)}),
    )

    def get_unique_number(self, obj):
        try:
            return obj.profile.unique_number
        except UserProfile.DoesNotExist:
            return "—"
    get_unique_number.short_description = "Уникальный номер"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'unique_number', 'user__email', 'user__date_joined')
    list_filter = ('user__is_active', 'user__is_staff')
    search_fields = ('user__username', 'user__email', 'unique_number')
    readonly_fields = ('user', 'unique_number')