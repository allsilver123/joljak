from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # 목록 페이지에 표시할 필드 추가
    list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'is_staff')
    # 필드셋에 'phone_number' 필드 추가 (선택적)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )
    # 사용자 생성 폼에 'phone_number' 필드 추가 (선택적)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )

# 기존의 CustomUser 모델 등록을 해제하고 CustomUserAdmin 클래스와 함께 다시 등록
admin.site.register(CustomUser, CustomUserAdmin)
