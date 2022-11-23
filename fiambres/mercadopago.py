import mercadopago
# Agrega credenciales
sdk = mercadopago.SDK("TEST-1953709056975791-070715-fee5a4518f04bb6b1d64977810e6cc39-127856537")

# Crea un ítem en la preferencia
preference_data = {
    "items": [
        {
            "title": "Mis productos",
            "quantity": 1,
            "total": 7,

        }
    ]
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]