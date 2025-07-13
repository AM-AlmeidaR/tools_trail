from datetime import datetime
from tools_trail.models import Herramienta, Operario

def get_current_year_context_processor(request):
    current_year = datetime.now().year
    return {
        'current_year': current_year
    }

def get_statistics_tools(request):
    return {
        'n_tools': Herramienta.objects.all().count(),
        'n_operario': Operario.objects.all().count(),
    }
