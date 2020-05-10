from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import views, registration

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.index_view, name="index"),
	path('select_target_word', views.select_target_word_view, name="select_target_word"),
	path('phrase', views.phrase_info_view, name="phrase_info"),
	path('phrase/similar_context_info', views.similar_context_info_view, name="similar-context-info"),
	path('phrase/similar_meaning_info', views.similar_meaning_info_view, name="similar-meaning-info"),
	path('phrase/similar_meaning_wordnet_info', views.similar_meaning_wordnet_info_view, name="similar-meaning-wordnet-info"),
	path('phrase/same_sound_info', views.same_sound_info_view, name="same-sound-info"),

	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
	path('signup/', registration.signup, name='signup'),
	path('update-user-level/', registration.update_user_options, name='update-user-options'),
]
