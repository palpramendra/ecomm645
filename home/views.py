from django.shortcuts import render,redirect
from .models import *
from django.views.generic import View
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


class BaseView(View):
    views = {}
    views['category'] = Category.objects.all()


class HomeView(BaseView):
    def get(self, request):
        self.views
        self.views['categories'] = Category.objects.all()
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['brands'] = Brand.objects.all()
        self.views['news'] = Product.objects.filter(labels='new')
        self.views['hots'] = Product.objects.filter(labels='hot')
        self.views['sales'] = Product.objects.filter(labels='sale')
        self.views['reviews'] = Review.objects.all()

        return render(request, 'index.html', self.views)


class CategoryView(BaseView):

    def get(self,request,slug):
        self.views
        ids = Category.objects.get(slug = slug).id
        self.views['catproducts'] = Product.objects.filter(category_id = ids)
        return render(request, 'category.html', self.views)

class ProductDetailView(BaseView):
    def get(self,request,slug):
        self.views
        self.views['productdetails'] = Product.objects.filter(slug = slug)
        subcat_ids = Product.objects.get(slug=slug).subcategory_id
        self.views['related_products'] = Product.objects.filter(subcategory_id=subcat_ids)
        self.views['product_review'] = ProductReview.objects.filter(slug=slug)
        return render(request, 'product-detail.html',self.views)

class SearchProduct(BaseView):
    def get(self,request):
        self.views
        if request.method == 'GET':
            query = request.GET['query']
            if query == '':
                return redirect('/')
            else:
                self.views['search_product'] = Product.objects.filter(name__icontains = query)
            return render(request, 'search.html', self.views)

def product_review(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        slug = request.POST['slug']
        review = request.POST['review']
        star = request.POST['star']
        x = datetime.datetime.now()
        date = x.strftime("%c")

        data = ProductReview.objects.create(
            name = name,
            email = email,
            slug = slug,
            review = review,
            star = star,
            date = date
        )
        data.save()
        return redirect(f'/product-detail/{slug}')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username = username).exits():
                messages.error(request, 'The username is already taken.')
                return redirect('/signup')
            if User.objects.filter(email = email).exits():
                messages.error(request, 'The email is already taken.')
                return redirect('/signup')
            else:
                user = User.objects.create_user(
                username = username,
                email = email,
                password = password
                )
                user.save()
                return redirect('/signup')
        else:
            messages.error(request, 'The password does not match')
            return redirect('/signup')
    return render(request,'signup.html')

class CartView(BaseView):
    def get(self,request):
        username = request.user.username
        self.views['view_cart']=Cart.objects.filter(username=username)
        return render(request,'cart.html', self.views)
def cart(request,slug):
    if Product.objects.filter(slug=slug).exists():
        username = request.user.username
        if Cart.objects.filter(slug=slug,username=username).exists():
            quantity = Cart.objects.get(slug=slug).quantity
            price = Cart.objects.get(slug=slug).price
            discounted_price = Cart.objects.get(slug=slug).discounted_price
            quantity = quantity + 1
            if discounted_price > 0:
                total = discounted_price*quantity
            else:
                total = price*quantity
            Cart.objects.get(slug=slug,username=username).update(quantity=quantity,total=total)
            return redirect('/cart')
        else:
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            if discounted_price > 0:
                total = discounted_price
            else:
                total = price
            data = Cart.objects.create(
                username=username,
                quantity=1,
                total=total,
                slug=slug,
                items=Product.objects.get(slug=slug)
            )
            data.save()
            return redirect('/cart')

def delete_cart(request,slug):
    username = request.user.username
    if Cart.objects.filter(slug=slug, username=username).exist():
        Cart.objects.filter(slug=slug, username=username).delete()
        return redirect('/')

def reduce_quantity(request,slug):
    if Product.objects.filter(slug=slug).exists():
        username = request.user.username
        if Cart.objects.filter(slug=slug, username=username).exists():
            quantity = Cart.objects.get(slug=slug).quantity
            price = Cart.objects.get(slug=slug).price
            discounted_price = Cart.objects.get(slug=slug).discounted_price
            if quantity > 1:
                quantity=quantity - 1
                if discounted_price > 0:
                    total = discounted_price * quantity
                else:
                    total = price * quantity
                Cart.objects.get(slug=slug, username=username).update(quantity=quantity, total=total)
                return redirect('/')
            else:
                messages.error(request, 'The quantity of the product is already 1.')
                return redirect('/')



# ---------------------------API----------------------------------

# ViewSets define the view behavior.
from .serializers import *
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['category', 'subcategory', 'stock', 'labels', 'brand']
    ordering_fields = ['id', 'price', 'name']
    search_fields = ['name', 'description', 'specification']



