def user_avatar_path(instance, filename):
    """
    Generate upload path for user avatars.
    File will be uploaded to MEDIA_ROOT/avatar/<username>/<filename>
    """
    ext = filename.split('.')[-1]

    folder_name = instance.username if instance.username else instance.email
    from django.utils import timezone
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"avatar_{timestamp}.{ext}"

    return f'avatar/{folder_name}/{new_filename}'