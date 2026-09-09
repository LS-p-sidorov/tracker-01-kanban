from functools import wraps

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BoardForm, RegisterForm, RoleForm, TaskForm
from .models import Board, Profile, Task


def manager_required(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        profile = getattr(request.user, "profile", None)
        if not profile or not profile.is_manager:
            messages.error(request, "Доступно только Менеджеру.")
            return redirect("board_list")
        return view(request, *args, **kwargs)

    return wrapper


@transaction.atomic
def register(request):
    if request.user.is_authenticated:
        return redirect("board_list")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        Profile.objects.create(user=user, role=Profile.Role.MEMBER)
        login(request, user)
        messages.success(request, "Регистрация завершена. Ваша роль — Участник.")
        return redirect("board_list")
    return render(request, "boards/register.html", {"form": form})


@login_required
def board_list(request):
    boards = Board.objects.order_by("-created_at")
    return render(request, "boards/board_list.html", {"boards": boards})


@manager_required
def board_create(request):
    form = BoardForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Доска создана.")
        return redirect("board_list")
    return render(request, "boards/board_form.html", {"form": form})


@login_required
def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    profile = getattr(request.user, "profile", None)
    columns = []
    for value, label in Task.Status.choices:
        cards = []
        for task in board.tasks.filter(status=value).order_by("created_at"):
            cards.append({"task": task, "movable": task.can_be_moved_by(request.user)})
        columns.append({"value": value, "label": label, "cards": cards})
    return render(
        request,
        "boards/board_detail.html",
        {
            "board": board,
            "columns": columns,
            "statuses": Task.Status.choices,
            "is_manager": bool(profile and profile.is_manager),
        },
    )


@login_required
def task_create(request, pk):
    board = get_object_or_404(Board, pk=pk)
    form = TaskForm(request.POST or None, initial={"board": board})
    form.fields["board"].queryset = Board.objects.filter(pk=board.pk)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.author = request.user
        task.save()
        messages.success(request, "Задача создана.")
        return redirect("board_detail", pk=board.pk)
    return render(request, "boards/task_form.html", {"form": form, "board": board})


@login_required
@require_POST
def task_move(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if not task.can_be_moved_by(request.user):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": False}, status=403)
        messages.error(request, "Вы можете перемещать только свои задачи.")
        return redirect("board_detail", pk=task.board_id)
    new_status = request.POST.get("status")
    if new_status not in Task.Status.values:
        return HttpResponseForbidden()
    task.status = new_status
    task.save(update_fields=["status"])
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True})
    return redirect("board_detail", pk=task.board_id)


@manager_required
def user_list(request):
    profiles = Profile.objects.select_related("user").order_by("user__username")
    if request.method == "POST":
        profile = get_object_or_404(Profile, pk=request.POST.get("profile_id"))
        form = RoleForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"Роль пользователя {profile.user.username} обновлена.")
        return redirect("user_list")
    return render(request, "boards/user_list.html", {"profiles": profiles})
