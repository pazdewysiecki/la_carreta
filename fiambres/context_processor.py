def total(request):
    total = 0
    total_carrito = 0
    if request.user.is_authenticated:
        if "cart" in request.session.keys():
            for key, value in request.session["cart"].items():
                total += float(value["quantity"])
                total_carrito += float(value["price"])
    return {"total": total, "total_carrito": total_carrito }
