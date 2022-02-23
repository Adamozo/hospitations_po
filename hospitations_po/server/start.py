def start():
    import os
    file = os.path.join('hospitations_po', 'server', 'main.py')
    os.system(f'poetry run python {file}')
