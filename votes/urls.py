from django.contrib import admin
from django.urls import path, include

from .views import ApprovalVoteView, DoneView, ApprovalResultView, HomeView, VoteView, FPTPResultView, FPTPVoteView, \
    STVVoteView, STVResultView, STVAllVoteView, UpdateElection, CreateElection, CreateCandidate, UpdateCandidate, AdminView, TicketView, ResultView

app_name = "votes"

urlpatterns = [
    path('', HomeView.as_view(), name="elections"),
    path('<int:election>/', VoteView.as_view(), name="vote"),
    path('<int:election>/approval/', ApprovalVoteView.as_view(), name="approval_vote"),
    path('<int:election>/fptp/', FPTPVoteView.as_view(), name="fptp_vote"),
    path('<int:election>/stv/', STVVoteView.as_view(), name="stv_vote"),
    path('<int:election>/<uuid:slug>/', DoneView.as_view(), name="vote_done"),
    path('<int:election>/results/', ResultView.as_view(), name="results"),
    path('<int:election>/results/approval/', ApprovalResultView.as_view(), name="approval_results"),
    path('<int:election>/results/fptp/', FPTPResultView.as_view(), name="fptp_results"),
    path('<int:election>/results/stv/', STVResultView.as_view(), name="stv_results"),
    path('<int:election>/results/stv/votes/', STVAllVoteView.as_view(), name="stv_all_votes"),
    path('admin/', AdminView.as_view(), name="admin"),
    path('admin/tickets/', TicketView.as_view(), name="tickets"),
    path('admin/create/', CreateElection.as_view(), name="create_election"),
    path('admin/edit/<int:election>/', UpdateElection.as_view(), name="update_election"),
    path('admin/edit/<int:election>/create/', CreateCandidate.as_view(), name="create_candidate"),
    path('admin/edit/<int:election>/edit/<int:candidate>/', UpdateCandidate.as_view(), name="update_candidate"),
]
