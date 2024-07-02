from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .models import Slider, Category, Cart, Course
from .models import Post
from .forms import CommentForm
from .models import Product
from django.shortcuts import redirect
from django.conf import settings
from django.utils.translation import activate


def my_view(request):
    activate('ar')  # Set language to Arabic


def set_language(request):
    lang_code = request.POST.get('language', settings.LANGUAGE_CODE)
    redirect_to = request.POST.get('next', '/')

    if lang_code and lang_code in dict(settings.LANGUAGES).keys():
        activate(lang_code)
        request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code

        # Ensure the redirect URL is safe
        if not redirect_to.startswith('/'):
            redirect_to = '/'

        # Update the URL to include the new language code
        parts = redirect_to.strip('/').split('/')
        if parts and parts[0] in dict(settings.LANGUAGES).keys():
            parts[0] = lang_code
        else:
            parts.insert(0, lang_code)
        redirect_to = '/' + '/'.join(parts)

    return redirect(redirect_to)


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def index(request):
    products = Product.objects.select_related('author').filter(featured=True)
    slides = Slider.objects.order_by('order')
    return render(
        request, 'index.html',
        {
            'products': products,
            'slides': slides
        }
    )


def product(request, pid):
    product = get_object_or_404(Product, pk=pid)
    comments = product.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product  # Associate comment with the product
            new_comment.save()
            return redirect('store.product', pid=pid)  # Redirect back to the same product detail page
    else:
        comment_form = CommentForm()

    return render(request, 'product.html', {'product': product, 'comment_form': comment_form, 'comments': comments})


def category(request, cid=None):
    cat = None

    query = request.GET.get('query')
    cid = request.GET.get('category', cid)
    where = {}
    if cid:
        cat = get_object_or_404(Category, pk=cid)
        where['category_id'] = cid

    if query:
        where['name__icontains'] = query

    products = Product.objects.filter(**where)
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'category.html', {
            'page_obj': page_obj,
            'category': cat
        }
    )


def cart(request):
    return render(
        request, 'cart.html'
    )


def cart_update(request, pid):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    cart_model = Cart.objects.filter(session=session_id).last()
    if cart_model is None:
        cart_model = Cart.objects.create(session_id=session_id, items=[pid])
    elif pid not in cart_model.items:
        cart_model.items.append(pid)
        cart_model.save()

    return JsonResponse({
        'message': _('The product has been added to your cart'),
        'items_count': len(cart_model.items)
    })


def cart_remove(request, pid):
    session_id = request.session.session_key

    if not session_id:
        return JsonResponse({})

    cart_model = Cart.objects.filter(session=session_id).last()
    if cart_model is None:
        return JsonResponse({})

    elif pid in cart_model.items:
        cart_model.items.remove(pid)
        cart_model.save()

    return JsonResponse({
        'message': _('The product has been removed from your cart'),
        'items_count': len(cart_model.items)
    })


def checkout(request):
    return render(
        request, 'checkout.html'
    )


def checkout_complete(request):
    Cart.objects.filter(session=request.session.session_key).delete()
    return render(
        request, 'checkout_complete.html'
    )


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})


def new_comment(request, pid):
    product = get_object_or_404(Product, pk=pid)
    comments = product.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.user = request.user
            new_comment.save()
            # Clear the form to prepare for another comment
            comment_form = CommentForm()  # Reset the form
    else:
        comment_form = CommentForm()

    return render(request, 'product.html', {'product': product, 'comment_form': comment_form, 'comments': comments})
