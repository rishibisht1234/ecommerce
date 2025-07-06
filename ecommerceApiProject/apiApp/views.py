from django.shortcuts import render
from .models import Product,Category,CustomUser,Cart,CartItem,Review
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductListSerializer,ProductDetailSerializer,CategoryListSerializer,CategoryDetailSerializer,CartItemSerializer,CartSerializer,CartStatSerializer,ReviewSerializer
from django.contrib.auth import get_user_model
# Create your views here.
@api_view(["GET"])
def product_list(request):
    products=Product.objects.filter(featured=True)
    serializer=ProductListSerializer(products,many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request,slug):
    product=Product.objects.get(slug=slug)
    serializer=ProductDetailSerializer(product)
    return Response(serializer.data)

@api_view(["GET"])
def category_list(request):
    categories=Category.objects.all()
    serializer=CategoryListSerializer(categories,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def category_detail(request,slug):
    catergory=Category.objects.get(slug=slug)
    serializer=CategoryDetailSerializer(catergory)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request):
    cart_code=request.data.get('cart_code')
    product_id=request.data.get('product_id')
    
    cart,created=Cart.objects.get_or_create(cart_code=cart_code)
    product=Product.objects.get(id=product_id)
    cartitem,created=CartItem.objects.get_or_create(product=product,cart=cart)
    cartitem.quantity = 1
    cartitem.save()
    
    serializer=CartSerializer(cart)
    return Response(serializer.data)

@api_view(['PUT'])
def update_cartitem_quantity(request):
    cartitem_id=request.data.get('item_id')
    quantity=request.data.get('quantity')
    quantity=int(quantity)
    cartitem=CartItem.objects.get(id=cartitem_id)
    cartitem.quantity=quantity
    cartitem.save()
    
    serializer=CartItemSerializer(cartitem)
    return Response({'data':serializer.data,'message':'cartitem updated successfully!'})

@api_view(["POST"])
def add_review(request):
    User=get_user_model() 
    product_id=request.data.get('product_id')
    email=request.data.get('email')
    review_text=request.data.get('review')
    rating=request.data.get('rating')
    
    
    product=Product.objects.get(id=product_id)
    user=User.objects.get(email=email)
    
    if Review.objects.filter(product=product,user=user).exists():
        return Response("You ALready Dropped a review for this product", status=400)
    
    review=Review.objects.create(product=product,user=user,rating=rating,review=review_text)
    serializer=ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['PUT'])
def update_review(request,pk):
    review=Review.objects.get(pk=pk)
    rating=request.data.get('rating')
    review_text=request.data.get('review')
    
    review.rating=rating
    review.review=review_text
    review.save()
    serializer=ReviewSerializer(review)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_review(request,pk):
    review=Review.objects.get(pk=pk)
    review.delete()
    return Response('Review deleted successfully',status=204)
    
    
    