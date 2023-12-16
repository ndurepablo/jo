@app.cli.command("createsuperuser")
def createsuperuser():

    while True:
        username = input("Enter username: ")
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print('El nombre de usuario ya está en uso. Por favor, elige otro.')
            continue

        email = input("Enter email: ")
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print('El email ya está en uso. Por favor, elige otro.')
            continue

        password = input("Enter password: ")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        is_admin = input("Is admin: ")

        user = User(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            last_name=last_name,
            first_name=first_name,
            is_admin=bool(is_admin)  # O establece el rol de superusuario como prefieras
        )

        db.session.add(user)
        db.session.commit()
        return "Superuser created successfully"