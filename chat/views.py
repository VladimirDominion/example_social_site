from django.shortcuts import render


def chat(request):
    user = request.user
    return render(
        request, "index.html", {
            'user': user,
        }
    )