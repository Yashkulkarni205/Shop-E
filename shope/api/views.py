from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer

import sys
sys.path.append("..")
from shop.models import Product
# Create your views here.
# django rest

@api_view(['GET'])
def api(request):
    urls = {
        'List':'api/api-list',
        'Create':'api/api-create',
        'Read':'api/api-read/id',
        'Update':'api/api-update/id',
        'Delete':'api/api=delete/id'
    }
    return Response(urls)

@api_view(['GET'])
def api_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many= True)
    return Response(serializer.data)

@api_view(['POST'])
def api_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def api_read(request,pk):
    products = Product.objects.get(id=pk)
    serializer = ProductSerializer(products, many= False)
    return Response(serializer.data)

@api_view(['POST'])
def api_update(request,pk):
    products = Product.objects.get(id=pk)
    serializer = ProductSerializer(instance=products,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def api_delete(request,pk):
    products = Product.objects.get(id=pk)
    products.delete()

    return Response("Item deleted")