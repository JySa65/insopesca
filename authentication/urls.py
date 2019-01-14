from authentication.views import UserListView, UserCreateView, UserUpdateView, \
    UserDeleteView, UserDetailView, ChangePassword, HomePageFormView, \
    SecurityQuestionCreateView
from django.urls import path

app_name = "authentication"

urlpatterns = [
    path('', UserListView.as_view(), name="list"),
    path('create/', UserCreateView.as_view(), name="create"),
    path('detail/<pk>/', UserDetailView.as_view(), name="detail"),
    path('update/<pk>/', UserUpdateView.as_view(), name="update"),
    path('delete/<pk>/', UserDeleteView.as_view(), name="delete"),
    path('detail/<pk>/security-question/create/',
         SecurityQuestionCreateView.as_view(),
         name="security_question"),

    # change password
    path('change_password/', ChangePassword.as_view(), name="change_password"),

]
