from django.shortcuts import redirect

class VerifiedRequiredMixin(object):
    """Allow user to stay at on ballot sheet."""
    def dispatch(self, request, *args, **kwargs):
        if 'voter' not in request.session:
            return redirect('votes:index')
        return super().dispatch(request, *args, **kwargs)
        
