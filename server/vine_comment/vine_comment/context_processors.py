from forms import VineRegistrationForm as registration_form
from vine_comment.views import get_author


def registration(request):
    return {"registration_form": registration_form}


def login(request):
    pass

def comment_author(request):
    author = get_author(request.user)
    return {"author": author}
