from django.contrib.auth.mixins import AccessMixin 
from django.shortcuts import redirect
class SuperRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('login')