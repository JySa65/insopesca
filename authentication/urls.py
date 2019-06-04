from django.urls import path

from authentication.views import UserListView, UserCreateView, UserUpdateView, \
    UserDeleteView, UserDetailView, ChangePassword, SecurityQuestionCreateView, \
    UserAdminDetailView, UserAdminUpdateView, RestoreDataUser, UserDetailApiView, \
    BackupBDView, BackupBDAPiView


app_name = "authentication"

urlpatterns = [
#     path('', UserListView.as_view(), name="list"),
    path('create/', UserCreateView.as_view(), name="create"),
    path('detail/<pk>/', UserDetailView.as_view(), name="detail"),
    path('update/<pk>/', UserUpdateView.as_view(), name="update"),
    path('delete/<pk>/', UserDeleteView.as_view(), name="delete"),
    path('detail/<pk>/security-question/create/',
         SecurityQuestionCreateView.as_view(),
         name="security_question"),

    # change password
    path('change-password/', ChangePassword.as_view(), name="change_password"),

    # Profile
    path('detail/',
         UserAdminDetailView.as_view(), name='detail_profile'),
    path('update/',
         UserAdminUpdateView.as_view(), name='update_profile'),

    path('restore-data/', RestoreDataUser.as_view(), name="restore_data"),

    # api

    path('api/detail/', UserDetailApiView.as_view(), name="api_detail_user"),

     # BD backup o restore
    path('bd/', BackupBDView.as_view(), name="bd_user"),
    path('api/bd/', BackupBDAPiView.as_view(), name="bd_api"),
]
