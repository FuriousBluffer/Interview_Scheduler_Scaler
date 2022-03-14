from django.urls import path

from interviews.views import CreateInterview, GetInterview, UpdateInterview, DeleteInterview, RetrieveInterview

urlpatterns = [
    path("", GetInterview.as_view(), name="interviews"),
    path("create/", CreateInterview.as_view(), name="create_interview"),
    path("update/<int:pk>/", UpdateInterview.as_view(), name="update_interview"),
    path("delete/<int:pk>/", DeleteInterview.as_view(), name="delete_interview"),
    path("retrieve/<int:pk>/", RetrieveInterview.as_view(), name="retrieve_interview"),
]
