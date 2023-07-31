def item_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / <instance.__class__.__name__>_<id>/<filename>
    return '{2}_{0}/{1}'.format(instance.id, filename, instance.__class__.__name__)