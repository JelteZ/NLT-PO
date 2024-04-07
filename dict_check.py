
dict = {
    1: {
        'name': {"first": "John", "last": "Doe"},
        'age': {"birthyear": 2001},
        'country': {"name": "USA", "state": "California"},
    },
    2: {
        'name': {"first": "Jane", "last": "Doe"},
        'age': {"birthyear": 2000},
        'country': {"name": "USA", "state": "California"},
    },
}

print(dict[1]['name']['first'])