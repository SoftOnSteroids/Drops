Epecificaciones
---
# Alcances

El objetivo de la aplicación es mostrar en un móvil o una web un detalle de las dosis a aplicar por cada evento, agrupadas por ojo. Debe haber un checkbox para registrar la gota aplicada. Debe sonar la alarma en el horario correcto y cada 5 minutos con posibilidad de snooze hasta completar todas las aplicaciones del evento. 

# Pantallas y especificaciones

## 1\. Home (day_timetable)

Calendar en vista semanal con el día de hoy seleccionado por defecto. Con una lista de los events del día seleccionado.
La vista del calendario es semanal por lo que el cálculo de eventos se hace sobre la semana solicitada, de domingo a sábado. *El usuario deberá contemplar si hay gotas que tienen frecuencias particulares par corregir el día de comienzo para cada semana (p.ej: si una gota se coloca día de por medio dependiendo cada semana cambiarán la cantidad de días de aplicación, algunas semanas se colocarán 4 días y otras 3)*

## 2\. Detalle de Event seleccionado (hour_timetable).

- Un **event** se componen de una lista de doses en un mismo horario de un determinado día. Event: \[Doses\], daytime.
    Es el resultado de una query que filtra y agrupa dosis por fecha y horario.
- Una **dosis** es una aplicación de un determinado medicamento a una determinada hora en un determinado día. Dosis: Dropper, daytime.

> 💡 Probar si se puede calcular de forma sencilla las dosis a medida que se consulta una determinada semana. La regla sería en modo lazy load, primero que si se modifica algún dato relevante del un dropper, se borran las dosis existentes del mismo en el rango de la fecha de inicio en adelante y se generan las nuevas para la semana actual (si la fecha de inicio la afecta). Las demás se generan cuando se consulta una semana específica, el backend comprueba si para la semana solicitada ya existe la muestra, de lo contrario la calcula y crea las dosis correspondientes.
> En una versión más pro, podría comprobarse si la operación borrará dosis y pedirle validación al usuario.

## 3\. Detalle de dropper o pastilla con ABM.
- La propiedad start_datetime se compone de dos partes, el día de comienzo de aplicación de las dosis y la hora. La hora de inicio y la frecuencia es la que se utilizará para la creación diaria de las dosis. 
- Se asume que las dosis comienzan a las 8am de cada día, se puede cambiar.
- La frecuencia es en horas.
    Cuando se carga o modifica la frecuencia u hora de inicio de algún dropper, se deben volver a regenerar los events.

## Dosis
El horario en las dosis se computará sin considerar el encadenamiento de dosificaciones, eso lo deberá contemplar el usuario. Por ejemplo si necesita esperar 5 minutos entre la aplicación de diferentes gota de un mismo horario para un mismo ojo. La aplicación plasmará el horario teórico para facilitar el agrupamiento en eventos de cada día.
```math

```

# Class Diagram

```mermaid
classDiagram
  Dropper "1" *-- "0...*" Dose : composition
  link Dropper "http://127.0.0.1:8000/droppers" "Link a droppers"
  class Dropper {
    +string name
    +string description
    +string code
    +int place_apply
    +int frequency
    +datetime start_datetime
    +date end_day
    +date date_expiration
    +list~Dose~ doses
    +getDoses(datetime? date_min, datetime? date_max) List~Dose~
    }
  link Dose "http://127.0.0.1:8000/doses"
  class Dose {
    +object_id dropper_id
    +datetime application_datetime
  }
```
Atributos modificados: place_apply, frequency, start_datetime, end_day, [doses]
# Formato del json que devolverá el API:

## Droppers

```json
[
  {
    "id":"6417b00c36a1f48e085739f6",
    "name":"Clorhexidina",
    "description":null,
    "code":"2904282",
    "place_apply": 1,
    "frequency": 6,
    "start_datetime": "2023-01-17 08:00:00",
    "end_day": "2023-06-17",
    "date_expiration":"2023-05-07"
  }
]
```

## Doses
```json
[
  {
    "id":"64206d35bfcdec8f747d86e0",
    "dropper_id":"6417e646f1a687ad69c5ac7d",
    "application_datetime":"2023-05-07 08:00:00"
  }
]
```

# ER Diagram

```mermaid
erDiagram
  DROPPER ||--|{ DOSE : origins
  DROPPER {
    ObjectID id PK
    string name
      string description
      string code
        int place_apply "1=left, 2=rear, 3=both"
      int frequency "in hours 1<f<24"
      datetime start_datetime "this day at 8am by default"
      date end_day "Infinite if not specified"
      date date_expiration
  }
  DOSE {
    ObjectID id PK
    ObjectID dropper_id FK
      datetime application_datetime
  }
```

# Dev

Iniciar MongoDB:
`brew services start mongodb-community`
Detener MongoDB:
`brew services stop mongodb-community`

Crear entorno virtual:
`python3 -m venv <path_virtual_env>`
Activar el entorno virtual:
`source <path_virtual_env>/bin/activate`
Desactivar el entorno virtual:
`deactivate`

Iniciar el server de desarrollo:
`uvicorn main:app --reload`
Detener el server: `Ctrl+C`

Documentación API con Swagger: http://127.0.0.1:8000/docs
Documentación API con Redocly: http://127.0.0.1:8000/redoc
