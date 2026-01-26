py -m venv venv
pip install -r requirements.txt
pip freeze > requirements.txt

Migraciones

Realizar una migracion
alembic revision --autogenerate -m "msg"

Subir a la base de datos
alembic upgrade head

Deshace la última migración (vuelve un paso atrás).
alembic downgrade -1

Muestra en qué versión está tu base de datos actualmente.	
alembic current	

Muestra el historial de migraciones.
alembic history	

Convertir ui a py
pyside6-uic pasante_id.ui -o pasante_ui.py 