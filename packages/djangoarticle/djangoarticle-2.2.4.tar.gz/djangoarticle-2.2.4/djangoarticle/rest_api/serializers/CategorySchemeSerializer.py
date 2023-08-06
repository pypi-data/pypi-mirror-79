from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField
from djangoarticle.models import CategoryModelScheme


class CategorySchemeSerializer(ModelSerializer):
    api_detail_url = HyperlinkedIdentityField(
        view_name = "djangoarticle:category_retrieve_viewset",
        lookup_field = "slug"
    )

    api_published_article_list_url = HyperlinkedIdentityField(
        view_name = "djangoarticle:category_detail_article_list_viewset",
        lookup_field = "slug",
        lookup_url_kwarg = "slug"
    )

    api_update_url = HyperlinkedIdentityField(
        view_name = "djangoarticle:category_update_viewset",
        lookup_field = "slug"
    )

    api_delete_url = HyperlinkedIdentityField(
        view_name = "djangoarticle:category_destroy_viewset",
        lookup_field = "slug"
    )

    detail_url = HyperlinkedIdentityField(
        view_name = "djangoarticle:category_detail_view",
        lookup_field = "slug",
        lookup_url_kwarg = "category_slug"
    )

    class Meta:
        model = CategoryModelScheme
        fields = ['serial', 'title', 'slug', 'description', 'author', 'status', 'verification',
                  'created_at', 'updated_at', 'api_detail_url', 'api_published_article_list_url',
                  'api_update_url', 'api_delete_url', 'detail_url']