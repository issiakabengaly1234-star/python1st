"""Fabrique de vues CRUD (liste, création, modification, suppression).

Chaque donnée est filtrée selon l'éleveur connecté : un utilisateur ne voit
et ne modifie que les fermes, animaux et opérations qui lui appartiennent
(les superutilisateurs voient tout).
"""
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError, Q
from django.shortcuts import redirect
from django.urls import path, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView


def owned(qs, user, lookup):
    if lookup and not user.is_superuser:
        return qs.filter(**{lookup: user})
    return qs


def restrict_form_choices(form, user):
    """Empêche de choisir la ferme, l'animal ou l'éleveur d'un autre utilisateur."""
    if user.is_superuser:
        return
    from accounts.models import Eleveur
    from animals.models import Animal
    from farms.models import Ferme

    for field in form.fields.values():
        if not isinstance(field, forms.ModelChoiceField):
            continue
        model = field.queryset.model
        if model is Ferme:
            field.queryset = field.queryset.filter(proprietaire__user=user)
        elif model is Animal:
            field.queryset = field.queryset.filter(ferme__proprietaire__user=user)
        elif model is Eleveur:
            field.queryset = field.queryset.filter(user=user)


class OwnedMixin(LoginRequiredMixin):
    owner_lookup = None

    def get_queryset(self):
        return owned(super().get_queryset(), self.request.user, self.owner_lookup)


def crud(model_class, form_cls, slug, route, title, new_label, columns,
         owner=None, search=(), related=(), chips=None, detail=None, on_create=None):
    names = {action: f"{slug}_{action}" for action in ("list", "create", "update", "delete")}
    if detail:
        names["detail"] = detail
    list_url = reverse_lazy(names["list"])
    base_ctx = {"title": title, "new_label": new_label, "columns": columns, "urls": names}

    class Base(OwnedMixin):
        model = model_class
        owner_lookup = owner

    class ListV(Base, ListView):
        template_name = "core/list.html"
        paginate_by = 25

        def get_queryset(self):
            qs = super().get_queryset()
            if related:
                qs = qs.select_related(*related)
            q = self.request.GET.get("q", "").strip()
            if q and search:
                condition = Q()
                for lookup in search:
                    condition |= Q(**{f"{lookup}__icontains": q})
                qs = qs.filter(condition)
            if chips:
                param, choices = chips
                value = self.request.GET.get(param, "")
                if value in dict(choices):
                    qs = qs.filter(**{param: value})
            return qs

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(base_ctx)
            params = self.request.GET.copy()
            params.pop("page", None)
            ctx["qs"] = params.urlencode()
            ctx["q"] = self.request.GET.get("q", "")
            ctx["searchable"] = bool(search)
            if chips:
                param, choices = chips
                current = self.request.GET.get(param, "")

                def link(value):
                    p = params.copy()
                    if value:
                        p[param] = value
                    else:
                        p.pop(param, None)
                    return "?" + p.urlencode()

                ctx["chip_param"] = param
                ctx["chip_current"] = current
                ctx["chips"] = [{"label": "Tous", "url": link(""), "active": not current}] + [
                    {"label": label, "url": link(value), "active": current == value}
                    for value, label in choices
                ]
            return ctx

    class FormBase(Base):
        form_class = form_cls
        success_url = list_url
        template_name = "core/form.html"

        def get_form(self, form_class=None):
            form = super().get_form(form_class)
            restrict_form_choices(form, self.request.user)
            return form

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(base_ctx)
            return ctx

        def form_valid(self, form):
            creating = form.instance.pk is None
            if creating and on_create:
                on_create(self.request, form.instance)
            response = super().form_valid(form)
            messages.success(
                self.request,
                "Enregistrement ajouté." if creating else "Modifications enregistrées.",
            )
            return response

    class CreateV(FormBase, CreateView):
        pass

    class UpdateV(FormBase, UpdateView):
        pass

    class DeleteV(Base, DeleteView):
        template_name = "core/confirm_delete.html"
        success_url = list_url

        def get_context_data(self, **kwargs):
            ctx = super().get_context_data(**kwargs)
            ctx.update(base_ctx)
            return ctx

        def form_valid(self, form):
            try:
                response = super().form_valid(form)
            except ProtectedError:
                messages.error(
                    self.request,
                    "Suppression impossible : d'autres enregistrements dépendent encore de cet élément.",
                )
                return redirect(names["list"])
            messages.success(self.request, "Enregistrement supprimé.")
            return response

    return [
        path(f"{route}/", ListV.as_view(), name=names["list"]),
        path(f"{route}/nouveau/", CreateV.as_view(), name=names["create"]),
        path(f"{route}/<int:pk>/modifier/", UpdateV.as_view(), name=names["update"]),
        path(f"{route}/<int:pk>/supprimer/", DeleteV.as_view(), name=names["delete"]),
    ]
