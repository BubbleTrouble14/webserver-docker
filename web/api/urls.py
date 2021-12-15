from django.urls import include, path
from rest_framework import routers
from .views import (
    BlockViewSet,
    CoinViewSet,
)

router = routers.DefaultRouter()
router.register('block', BlockViewSet)
router.register('coin', CoinViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    # path('giveaway/closest', ClosestTicketView.as_view()),
    # path('login', LoginView.as_view()),
    # path('login_qr', LoginQRView.as_view()),
    # path('qrcode', QRCodeView.as_view()),
    # path('loggedin', LoggedInView.as_view()),
    # path('stats', StatsView.as_view()),
    # path('xchscan_stats', XCHScanStatsView.as_view()),
    # path('space', SpaceView.as_view()),
]