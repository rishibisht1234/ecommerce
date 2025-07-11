from rest_framework import serializers
from .models import Product,Category,CustomUser,Cart,CartItem,Review,WishList,EcoTag
from django.contrib.auth import get_user_model

class EcoTagSerializer(serializers.ModelSerializer):
    class Meta:
        model=EcoTag
        fields=['id','name']

class ProductListSerializer(serializers.ModelSerializer):
    eco_tag=EcoTagSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields=('id','name','slug','image','price','eco_tag')

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=('id','name','slug','description','image','price')
        
class CategoryListSerializer(serializers.ModelSerializer):
    # products=ProductListSerializer(many=True,read_only=True)
    class Meta:
        model=Category
        fields=('id','name','image','slug')


class CategoryDetailSerializer(serializers.ModelSerializer):
    products=ProductListSerializer(many=True,read_only=True)
    class Meta:
        model=Category
        fields=('id','name','image','products')
        
        
class CartItemSerializer(serializers.ModelSerializer):
    product=ProductListSerializer(read_only=True)
    sub_total=serializers.SerializerMethodField()
    class Meta:
        model=CartItem
        fields=('id','cart',"product","quantity","sub_total")
        
    def get_sub_total(self,cart_item):
        total=cart_item.product.price * cart_item.quantity
        return total
        
        
class CartSerializer(serializers.ModelSerializer):
    cart_items=CartItemSerializer(many=True,read_only=True)
    cart_total=serializers.SerializerMethodField()
    class Meta:
        model=Cart
        fields=['id','cart_code','cart_items','cart_total']
        
    def get_cart_total(self,cart):
        items=cart.cart_items.all()
        total=sum([item.quantity*item.product.price for item in items ])
        return total
    

            
class CartStatSerializer(serializers.ModelSerializer):
    total_quantity=serializers.SerializerMethodField()
    
    class Meta:
        model=Cart
        fields=['id','cart_code','total_quantity']
        
    def get_total_quantity(self,cart):
        items=cart.cart_items.all()
        total=sum([item.quantity for item in items])
        return total
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=['id','first_name','last_name','profile_picture_url']
    
class ReviewSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Review
        fields=['id','user','rating','review','created','updated']
        
class WishListSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    product=ProductListSerializer(read_only=True)
    class Meta:
        model=WishList
        fields=['id','user','product','created']