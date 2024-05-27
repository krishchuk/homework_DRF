from django.contrib import admin

from users.models import User, Pay


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "city",
    )


@admin.register(Pay)
class AdminPay(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "pay_date",
        "paid_course",
        "paid_lesson",
        "payment_amount",
        "payment_method",
        "session_id",
        "link",
    )
