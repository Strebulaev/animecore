from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"

class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='items')
    anime = models.ForeignKey('anime.Anime', on_delete=models.CASCADE)
    episode_number = models.IntegerField(null=True, blank=True)
    source_url = models.URLField()
    dub_studio = models.ForeignKey('dubs.DubGroup', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['episode_number', 'created_at']
        unique_together = ['playlist', 'anime']

    def __str__(self):
        return f"{self.playlist.title}: {self.anime.title_ru}"
