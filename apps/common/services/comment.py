from imobiledevice import BaseService

from apps.reaction.models import Comment


class CommentService:
    @staticmethod
    def get_comment_by_id(comment_id):
        comment = Comment.objects.get(id=comment_id)
        return comment