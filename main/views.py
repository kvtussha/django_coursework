from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.forms import MailingForm
from main.models import Mailing


class MailingListView(ListView):
    model = Mailing
    template_name = 'main/mailing/mailing_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'main/mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        return self.object


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing-list')
    template_name = 'main/mailing/mailing_form.html'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing/mailing_form.html'

    def get_success_url(self):
        return reverse('main:mailing-detail', kwargs={'pk': self.object.pk})


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'main/mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('main:mailing-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление рассылки'
        return context


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        print(f'{name}: {email}')
    return render(request, 'main/contacts.html')
