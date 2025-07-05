def cart_context(request):
    cart = request.session.get('cart', {})
    cart_item_count = 0

    # Suma la cantidad de cada item en el carrito
    for item in cart.values():
        cart_item_count += item.get('quantity', 0)

    return {
        'cart_item_count': cart_item_count
    }