from django.shortcuts import render, redirect
from products.models import Product, Comment
from products.forms import ProductCreateForms, CommentCreateForms
from products.constants import PAGINATION_LIMIT
from django.views.generic import CreateView, DetailView, ListView, DeleteView


class ManePageCBV(ListView):
    model = Product


class ProductCBV(ListView):
    model = Product
    template_name = 'products/products.html'

    def get(self,request, *args, **kwargs):
        products = self.get_queryset().order_by('-rate')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search:
            products = products.filter(title__contains=search) or products.filter(description__contains=search)

        max_page = products.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]

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
            ],
            'user': request.user,
            'pages': range(1, max_page + 1)
        }
        return render(request, self.template_name, context=context)


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


class CreateCBV(ListView, CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductCreateForms

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': self.form_class if not kwargs.get('form') else kwargs['form']
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, **kwargs):
        data, files = request.POST, request.FILES

        form = self.form_class(data, files)

        if form.is_valid():
            self.model.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate'),
            )
            return redirect('/products')
        return render(request, self.template_name, context=self.get_context_data())


