import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import os, shutil


print("MYSQLDUMP_PATH:", os.environ.get("MYSQLDUMP_PATH"))
print("MYSQL_CLIENT_PATH:", os.environ.get("MYSQL_CLIENT_PATH"))
print("mysqldump via shutil.which:", shutil.which("mysqldump"))
print("mysql via shutil.which:", shutil.which("mysql"))
print("mysqldump path exists:", Path(os.environ.get("MYSQLDUMP_PATH","")).exists())
print("mysql client path exists:", Path(os.environ.get("MYSQL_CLIENT_PATH","")).exists())
from herramientas.BD import respaldo_desde_url
respaldo_desde_url("mysql+pymysql://root@127.0.0.1/gestion_pasantes")