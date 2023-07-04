import os

import dotenv
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import AppUser
from .models import Sympathy
from .serializers import SympathySerializer, AppUserSerializer
from .utils import check_sympathy, calc_distance

# Load .env file
dotenv.load_dotenv()


class AppUserCreateView(generics.CreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [AllowAny]


class AppUserListView(LoginRequiredMixin, generics.ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('gender', 'first_name', 'last_name')

    def get_queryset(self):
        queryset = AppUser.objects.all()

        if self.request.query_params.get('max_distance') is None:
            # return the queryset as is
            return queryset
        # filter the queryset
        else:
            filtered_ids = []
            max_distance = float(self.request.query_params.get('max_distance'))

            for user in queryset:
                dist = calc_distance(self.request.user.id, user.id)
                if dist > max_distance:
                    filtered_ids.append(user.id)
                queryset = AppUser.objects.exclude(id__in=filtered_ids).exclude(id=self.request.user.id)

            return queryset


class SympathyCreateView(LoginRequiredMixin, generics.CreateAPIView):
    queryset = Sympathy.objects.all()
    serializer_class = SympathySerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'head', 'post']

    def get(self, request, *args, **kwargs):

        from_user = get_object_or_404(AppUser, id=request.user.id)
        to_user = get_object_or_404(AppUser, id=kwargs.get('id'))

        if from_user == to_user:
            return JsonResponse({'message': "You can't like your profile"})

        is_ids_exist = Sympathy.objects.filter(from_user=from_user, to_user=to_user).exists()

        if not is_ids_exist:
            Sympathy.objects.create(from_user=from_user, to_user=to_user)

        is_mutual_sympathy = check_sympathy(from_user, to_user)

        if is_mutual_sympathy:

            try:
                send_mail(
                    subject='Взаимная симпатия',
                    message=f'Вы понравились {to_user.first_name}! Почта участника: {to_user.email}',
                    from_email=os.getenv('EMAIL_HOST_USER'),
                    recipient_list=[from_user.email, ],
                    fail_silently=False,
                )

                send_mail(
                    subject='Взаимная симпатия',
                    message=f'Вы понравились {from_user.first_name}! Почта участника: {from_user.email}',
                    from_email=os.getenv('EMAIL_HOST_USER'),
                    recipient_list=[to_user.email, ],
                    fail_silently=False,
                )
                email_status = 'Emails sent!'

            except Exception as e:
                email_status = e

            return JsonResponse({'message': 'Match!',
                                 'email_status': str(email_status)})
        else:
            return JsonResponse({'message': 'No match!'})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'api/list'))
        else:
            return HttpResponse('Invalid email or password.')

    csrf_token = request.META.get('CSRF_COOKIE', '')
    return HttpResponse(f'''
        <form method="post">
            <input type="hidden" name="next" value="{{ request.GET.next }}">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <input type="text" name="email" placeholder="Email"><br>
            <input type="password" name="password" placeholder="Password"><br>
            <input type="submit" value="Log in">
        </form>
    ''')
