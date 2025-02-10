def profile_menu_items(request):
    menu = [
        {
            "title": "Информация",
            "url_name": "users:profile_detail",
            "icon": "bi-person-circle"
        },
        {
            "title": "Редактировать профиль",
            "url_name": "users:profile_edit",
            "icon": "bi-pencil-square"
        },
        {
            "title": "Сменить пароль",
            "url_name": "users:profile_password",
            "icon": "bi-key"
        },
    ]
    
    if request.resolver_match:
        current_url_name = request.resolver_match.url_name
        for item in menu:
            item['is_active'] = current_url_name == item['url_name']
    
    return {'profile_menu_items': menu}
