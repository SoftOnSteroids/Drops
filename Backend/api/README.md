Iniciar MongoDB:
```brew services start mongodb-community```
Detener MongoDB:
```brew services stop mongodb-community```

Crear entorno virtual:
```python3 -m venv <path_virtual_env>```
Activar el entorno virtual:
```source <path_virtual_env>/bin/activate```
Desactivar el entorno virtual:
```deactivate```

Iniciar el server de desarrollo:
```uvicorn main:app --reload```
Detener el server: ```Ctrl+C```

Documentación API con Swagger: http://127.0.0.1:8000/docs
Documentación API con Redocly: http://127.0.0.1:8000/redoc