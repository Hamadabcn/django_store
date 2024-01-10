from store.models import Category, Cart, Product


def store_website(request):
    cart = Cart.objects.filter(session=request.session.session_key).last()

    cart_total = 0
    cart_products = []

    if cart:
        cart_products = Product.objects.filter(pk__in=cart.items)
        for item in cart_products:
            cart_total += item.price

    categories = Category.objects.order_by('order')
    return{
        'categories': categories,
        'cart_products': cart_products,
        'cart_total': cart_total
    }
