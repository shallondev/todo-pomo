from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid

# Authenticated User
class User(AbstractUser):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=70, unique=True) 

    def __str__(self):
        return self.name


# Notes
class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    title = models.CharField(max_length=70, unique=False)
    markdown_content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="notes")

    def __str__(self):
        return f"{self.title} created by {self.owner.username} on {self.created_at}"

    # Share a note with other uses
    def share_with_user(self, shared_user, can_edit=False):
        shared_note = SharedNote.objects.get_or_create(
            note=self,
            shared_user=shared_user,
            defaults={'can_edit': can_edit}
        )
        return shared_note

    # Delete association of note sharing
    def stop_sharing_with_user(self, shared_user):
        try:
            shared_note = SharedNote.objects.get(note=self, shared_user=shared_user)
            shared_note.delete()
        except SharedNote.DoesNotExist:
            pass


# Shared Notes
class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shared_with_users')
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')
    can_edit = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.note} shared with {self.shared_user}"

    # Toggle if shared user can edit 
    def toggle_editing(self):
        self.can_edit = not self.can_edit
        self.save()
        return self.can_edit


