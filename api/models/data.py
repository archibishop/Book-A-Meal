users = [
    {
        'id': 1,
        'first_name': 'dennis',
        'last_name': 'lubega',
        'email': 'lubega@gmail.com',
        'password': '12345',
    },
    {
        'id': 2,
        'first_name': 'atlas',
        'last_name': 'Tegz',
        'email': 'atlas@gmail.com',
        'password': '12345',
    }
]

admin = {
    'id': 1,
    'business_name': 'HAPPY FOODS',
    'location': 'NAKULABYE',
    'first_name': 'steven',
    'last_name': 'walube',
    'email': 'steven@gmail.com',
    'password': '54321',
}

meals = [
    {
        'id': 1,
        'meal_name': "ricebeans",
        'price': 3000,
        'meal_type': "lunch"
    },
    {
        'id': 2,
        'meal_name': 'rolex',
        'price': 4000,
        'meal_type': 'lunch'
    }
]

""" Need add date to this """
transactions = [
    {
        'id': 1,
        'meal_name': "ricebeans",
        'price': 3000,
        'user_id': 1,
        'process_status': "pending"
    },
    {
        'id': 2,
        'meal_name': "lasagna",
        'price': 10000,
        'user_id': 2,
    },
    {
        'id': 3,
        'meal_name': 'rolex',
        'price': 4000,
        'user_id': 1,
    }
]

menu_day = [
    {
        'id': 1,
        'meal_name': "ricebeans",
        'price': 3000,
        'meal_type': "lunch"
    },
    {
        'id': 2,
        'meal_name': "lasagna",
        'price': 10000,
        'meal_type': "breakfast"
    },
    {
        'id': 3,
        'meal_name': "Rice and Matooke",
        'price': 10000,
        'meal_type': "lunch"
    },
    {
        'id': 4,
        'meal_name': 'rolex',
        'price': 4000,
        'meal_type': "lunch"
    }
]
