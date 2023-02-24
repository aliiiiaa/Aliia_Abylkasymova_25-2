from django.shortcuts import render, redirect
from products.models import Product, Comment
from products.forms import ProductCreateForms, CommentCreateForms


# Create your views here.

def main_page_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()

        context = {
            'products': [
                {
                    'id': product.id,
                    'title': product.title,
                    'rate': product.rate,
                    'image': product.image,
                    'hashtags': product.hashtags.all()

                }
                for product in products
            ]
        }
        return render(request, 'products/products.html', context=context)


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)

        context = {
            'product': product,
            'comments': product.comment_set.all(),
            'form': CommentCreateForms,
        }

        return render(request, 'products/detail.html', context=context)

    if request.method == 'POST':
        data = request.POST
        form = CommentCreateForms(data=data)
        product = Product.objects.get(id=id)

        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data.get('text'),
                product=product
            )

        context = {
            'product': product,
            'comment': product.comment_set.all(),
            'form': form
        }
        return render(request, 'products/detail.html', context=context)


def create_product_view(request):
    if request.method == "GET":
        return render(request, 'products/create.html')

    if request.method == 'POST':
        data = request.POST

        errors = {}

        if len(data['title']) < 1 or len(data['title']) > 15:
            errors['title'] = 'Title error!'

        if len(data['description']) < 1 or len(data['description']) > 200:
            errors['description'] = 'description error!'

        if len(errors.keys()) < 1:
            Product.objects.create(
                title=data['title'],
                description=data['description'],
                rate=data['rate']
            )
            return redirect('/products')

        return render(request, 'products/create.html', context={
            'errors': errors
        })


