from django.db.models import Max

def item_directory_path(instance, filename):
    # Because before create a category it does not have any id
    # so need to get next availabe id from db
    # also, instance has not access to its class, so use __class__:

    users = instance.__class__.objects.all()
    #might be possible model has no records so make instance.__class__ to handle None
    next_id = users.aggregate(Max('id'))['id__max'] + 1 if users else 1
    # file will be uploaded to MEDIA_ROOT / <instance.__class__.__name__>_<id>/<filename>
    return '{2}_{0}/{1}'.format(next_id, filename, instance.__class__.__name__)