from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.forms import SendingForm
from main.models import Sending


class SendingListView(ListView):
    model = Sending
    template_name = 'main/sending/sending_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by(
            'status',  # Сначала сортируем по статусу
            'scheduled_time'  # Затем сортируем по времени рассылки в возрастающем порядке
        )
        return queryset


class SendingDetailView(DetailView):
    model = Sending
    template_name = 'main/sending/sending_detail.html'
    context_object_name = 'sending'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        return self.object


class SendingCreateView(CreateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy('main:sending-list')
    template_name = 'main/sending/sending_form.html'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class SendingUpdateView(UpdateView):
    model = Sending
    form_class = SendingForm
    template_name = 'main/sending/sending_form.html'

    def get_success_url(self):
        return reverse('main:sending-detail', kwargs={'pk': self.object.pk})


class SendingDeleteView(DeleteView):
    model = Sending
    template_name = 'main/sending/sending_confirm_delete.html'
    success_url = reverse_lazy('main:sending-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление поста'
        return context
