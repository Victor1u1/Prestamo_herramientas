import re
from django.conf import settings
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

    def __call__(self, request):
        # Verificar acceso al admin - usar el admin estándar de Django
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return redirect('/admin/login/')
            elif not (request.user.is_staff and request.user.is_admin):
                return redirect('error')
        
        # Verificar otras URLs protegidas
        elif not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(url.match(path) for url in self.exempt_urls):
                return redirect('error')
        
        response = self.get_response(request)
        return response
