from forms import VineRegistrationForm as registration_form


def registration(request):
    return {"registration_form": registration_form}


def login(request):
    pass


