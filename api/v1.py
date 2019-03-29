from api.orders_api import *
from api.news_api import *
from api.matches_api import *
from api.storage_api import *

def init(app, auth):
    api = Api(app)
    api.add_resource(NewsListApi, '/api/v1/news', resource_class_args=[auth])
    api.add_resource(NewsApi, '/api/v1/news/<int:id>', resource_class_args=[auth])
    api.add_resource(OrdersApi, '/api/v1/orders/<int:id>', resource_class_args=[auth])
    api.add_resource(MatchesListApi,'/api/v1/matches', resource_class_args=[auth])
    api.add_resource(StorageApi,'/api/v1/storage', resource_class_args=[auth])
