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

def convertir_a_romano(numero):

    
    # Mapeo de valores
    roman_map = {
        1000: 'M', 900: 'CM', 500: 'D', 400: 'CD',
        100: 'C', 90: 'XC', 50: 'L', 40: 'XL',
        10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'
    }
    
    # Conversión
    resultado = []
    for valor in sorted(roman_map.keys(), reverse=True):
        while numero >= valor:
            resultado.append(roman_map[valor])
            numero -= valor
    
    return ''.join(resultado)

def fecha_espanol(fecha):
    meses = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    mes = meses[fecha.month - 1]
    return f"{fecha.day} de {mes} de {fecha.year}"

def formato_miles(valor):
    if valor is None: return "0"
    # Formatea con coma (1,500) y luego reemplaza por punto (1.500)
    return "{:,.0f}".format(valor).replace(",", ".")
