from rest_framework.routers import DefaultRouter

from advertisements.views import AdvertisementViewSet

router = DefaultRouter()
router.register('advertisements', AdvertisementViewSet)

urlpatterns = router.urls