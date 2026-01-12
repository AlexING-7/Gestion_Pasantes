from datetime import date

def null_string(string):
    if not string:
        return ""
    else:
        return string
    
def calcular_edad(fecha_nacimiento: date | None) -> int | None:
        """Devuelve la edad en años a partir de una fecha (objeto date)."""
        if not fecha_nacimiento:
            return None
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        return edad

def calcular_duracion_meses(inicio: date | None, final: date | None) -> int | None:
    """Devuelve la duración en meses entre dos fechas (aproximada en meses completos).

    Si `inicio` o `final` es None devuelve None.
    """
    if not inicio or not final:
        return None
    # Si final es anterior a inicio, devolver 0
    if final < inicio:
        return 0
    años = final.year - inicio.year
    meses = final.month - inicio.month
    dias_correction = 1 if final.day < inicio.day else 0
    total_meses = años * 12 + meses - dias_correction
    return total_meses