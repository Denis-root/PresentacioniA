from datetime import datetime, timezone


def iso_to_utc_timestamps(start_iso: str, end_iso: str) -> tuple[int, int]:
    """
    Convierte dos fechas en formato ISO 8601 a timestamps en UTC.

    Args:
        start_iso (str): Fecha inicial en formato ISO (ej: '2025-04-21T18:00:00')
        end_iso (str): Fecha final en formato ISO (ej: '2025-04-22T18:00:00')

    Returns:
        tuple: (timestamp_inicio_utc, timestamp_final_utc)
    """
    start_dt = datetime.fromisoformat(start_iso).replace(tzinfo=timezone.utc)
    end_dt = datetime.fromisoformat(end_iso).replace(tzinfo=timezone.utc)

    return int(start_dt.timestamp()), int(end_dt.timestamp())


def get_current_local_iso(offset_hours: int = -6) -> str:
    """
    Retorna la fecha y hora actual ajustada a una zona horaria específica (por defecto GMT-6), en formato ISO 8601.

    Args:
        offset_hours (int): Desfase horario respecto a UTC. Ej: -6 para GMT-6

    Returns:
        str: Fecha y hora local en formato ISO 8601
    """
    from datetime import datetime, timedelta, timezone

    local_tz = timezone(timedelta(hours=offset_hours))
    return datetime.now(local_tz).isoformat()


def obtener_bloques_disponibles(eventos, hora_inicio_str='08:00', hora_fin_str='17:00'):
    from datetime import datetime, time, timedelta
    import pytz
    from collections import defaultdict

    zona_horaria = pytz.timezone('America/El_Salvador')
    hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
    hora_fin = datetime.strptime(hora_fin_str, '%H:%M').time()

    eventos_por_dia = defaultdict(list)
    for evento in eventos:
        inicio_str = evento['start']['dateTime']
        fin_str = evento['end']['dateTime']
        inicio = datetime.fromisoformat(inicio_str).astimezone(zona_horaria)
        fin = datetime.fromisoformat(fin_str).astimezone(zona_horaria)
        fecha = inicio.date()
        eventos_por_dia[fecha].append((inicio, fin))

    resultados = []

    for fecha, bloques_ocupados in eventos_por_dia.items():
        inicio_dia = zona_horaria.localize(datetime.combine(fecha, hora_inicio))
        fin_dia = zona_horaria.localize(datetime.combine(fecha, hora_fin))

        bloques_ocupados.sort()
        disponibles = []
        actual = inicio_dia

        for inicio_evento, fin_evento in bloques_ocupados:
            # Si el evento empieza después del horario permitido, lo ignoramos
            if inicio_evento >= fin_dia:
                continue

            # Cortamos el inicio del evento si comienza antes del inicio del rango
            inicio_evento = max(inicio_evento, inicio_dia)
            # Cortamos el final del evento si termina después del fin del rango
            fin_evento = min(fin_evento, fin_dia)

            if inicio_evento > actual:
                disponibles.append({
                    'inicio': actual.strftime('%H:%M'),
                    'fin': inicio_evento.strftime('%H:%M')
                })
            actual = max(actual, fin_evento)

        if actual < fin_dia:
            disponibles.append({
                'inicio': actual.strftime('%H:%M'),
                'fin': fin_dia.strftime('%H:%M')
            })

        resultados.append({
            'fecha': fecha.isoformat(),
            'disponibles': disponibles
        })

    return resultados



def parse_local_datetime(fecha_texto: str, offset="-06:00") -> str:
    from dateutil.parser import parse
    try:
        dt = parse(fecha_texto)
        return dt.strftime(f"%Y-%m-%dT%H:%M:%S{offset}")
    except Exception as e:
        raise ValueError(f"Formato de fecha inválido: '{fecha_texto}' → {e}")
