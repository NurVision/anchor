from django.utils.translation import get_language

from apps.item.models import Category


class CategoryService:

    @staticmethod
    def get_category_tree(category):
        """Get categories organized by hierarchy"""
        current_lang = get_language()

        root_categories = Category.objects.filter(parent=None)

        tree = []
        for root in root_categories:
            tree.append({
                'category': root,
                'title': getattr(root, f'title_{current_lang}', root.title),
                'slug': getattr(root, f'slug_{current_lang}', root.slug),
                'children': root.children.all()
            })

        return tree
