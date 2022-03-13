# hospitations_po

Project of system that can help during academical teachers audit process. I started woring on that project during one of my acedemical coursers but I am still imporving it and adding new things. Backend is created with use of FastApi and PostgrreSQL as database. At this moment client desktop app is written with use of tkinter.  

<br />
<br />
<br />

# Instalation and run guide

## This project requiers:
* [postgres](https://linuxize.com/post/how-to-install-postgresql-on-debian-10/)
* python3
* [poetry](https://python-poetry.org/docs/)



At the begining create empty postgres database.
Paste connection link to your database in 
* hospitations_po/server/alembic.ini
* hospitations_po/server/database.py

\
To install all modules and dependencies execute bellow command in project directory.
<!-- Code Blocks -->
```bash
 poetry install
```

\
To create test database structure execute bellow commands from main project directory.
<!-- Code Blocks -->
```bash
 cd tests
 poetry run alembic -x data=true upgrade head
```

\
To create main database make sure that you replace database connection link with your own in hospitations_po/server/alembic.ini line 55.
<!-- Code Blocks -->
```bash
 cd hospitations_po/server
 poetry run alembic upgrade head
```

\
To start server make sure that you replace database connection link with your own in hospitations_po/server/database.py and then execute bellow commands from main project directory.
<!-- Code Blocks -->
```bash
 poetry run start_server
```

\
To start client run below command in new terminal.
<!-- Code Blocks -->
```bash
 poetry run start_gui
```
