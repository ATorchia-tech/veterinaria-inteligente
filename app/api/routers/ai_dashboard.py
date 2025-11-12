from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from datetime import date

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def ai_dashboard():
    """Dashboard de predicción de afluencia con IA - Rediseñado sin scroll"""
    today = date.today().isoformat()
    # Obtener fecha formateada en español
    from datetime import datetime
    now = datetime.now()
    fecha_formateada = now.strftime('%A %d de %B de %Y').title()
    
    html_content = f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>🤖 Predicción de Afluencia - Veterinaria Inteligente</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); height: 100vh; overflow: hidden; }}
    .container {{ height: 100vh; display: flex; flex-direction: column; }}
    header {{ text-align: center; padding: 0.5rem 1rem; background: rgba(255,255,255,0.98); border-bottom: 2px solid #f59e0b; flex-shrink: 0; }}
    header h1 {{ margin: 0; font-size: 1.3rem; color: #333; font-weight: 700; display: inline-flex; align-items: center; gap: 0.4rem; }}
    header h1 .emoji {{ font-size: 1.5rem; }}
    header p {{ margin: 0.2rem 0 0; color: #666; font-size: 0.7rem; }}
    .nav-links {{ display: flex; flex-wrap: wrap; gap: 0.4rem; justify-content: center; align-items: center; padding: 0.5rem 1rem; background: rgba(255,255,255,0.95); border-bottom: 1px solid #f59e0b; flex-shrink: 0; }}
    .nav-links a {{ padding: 0.35rem 0.7rem; background: #fff7ed; color: #4a5568; text-decoration: none; border-radius: 6px; font-size: 0.7rem; transition: all 0.2s; border: 1px solid #fed7aa; white-space: nowrap; }}
    .nav-links a:hover {{ background: #f59e0b; color: #fff; transform: translateY(-1px); box-shadow: 0 2px 8px rgba(245,158,11,0.4); }}
    .btn-predict {{ padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 700; border: none; border-radius: 6px; cursor: pointer; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #fff; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3); transition: all 0.2s; white-space: nowrap; }}
    .btn-predict:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(245, 158, 11, 0.5); }}
    .header-info {{ padding: 0.6rem 1rem; background: rgba(255,255,255,0.95); border-bottom: 1px solid #f59e0b; flex-shrink: 0; }}
    .header-info-content {{ max-width: 1600px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.7rem; line-height: 1.4; color: #4a5568; align-items: center; }}
    .header-info-content strong {{ color: #2d3748; }}
    .header-info-box {{ padding: 0.4rem 0.6rem; background: #fef3c7; border-left: 3px solid #fbbf24; border-radius: 4px; flex: 0 0 auto; }}
    .main-content {{ flex: 1; overflow-y: auto; padding: 0.8rem; background: rgba(255,255,255,0.95); }}
    .content-grid {{ display: grid; grid-template-columns: 1fr 2fr; gap: 0.8rem; height: 100%; max-width: 1600px; margin: 0 auto; }}
    .left-column, .right-column {{ display: flex; flex-direction: column; gap: 0.8rem; }}
    .card {{ background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; display: flex; flex-direction: column; }}
    .card-header {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 0.6rem 1rem; font-weight: 700; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem; }}
    .card-body {{ padding: 0.8rem; flex: 1; overflow-y: auto; }}
    .info-text {{ font-size: 0.75rem; line-height: 1.4; color: #4a5568; margin-bottom: 0.5rem; }}
    .info-text strong {{ color: #2d3748; }}
    .current-data {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; }}
    .data-item {{ background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border: 2px solid #60a5fa; border-radius: 6px; padding: 0.5rem; text-align: center; }}
    .data-item .icon {{ font-size: 1.5rem; }}
    .data-item .value {{ font-size: 1.2rem; font-weight: 700; color: #1e40af; margin: 0.2rem 0; }}
    .data-item .label {{ font-size: 0.7rem; color: #3730a3; font-weight: 600; }}
    .forecast-mini {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.4rem; margin-top: 0.5rem; }}
    .forecast-mini-item {{ background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 6px; padding: 0.4rem; text-align: center; font-size: 0.7rem; }}
    .forecast-mini-item .day {{ font-weight: 700; color: #0c4a6e; margin-bottom: 0.2rem; }}
    .forecast-mini-item .temp {{ font-size: 1rem; color: #0369a1; font-weight: 700; }}
    .btn-action {{ padding: 0.7rem; font-size: 0.85rem; font-weight: 700; border: none; border-radius: 8px; cursor: pointer; transition: all 0.2s; text-decoration: none; display: block; text-align: center; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #fff; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3); }}
    .btn-action:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4); }}
    .btn-secondary {{ background: #f7fafc; color: #4a5568; border: 2px solid #e2e8f0; }}
    .btn-secondary:hover {{ background: #e2e8f0; }}
    #results {{ display: none; height: 100%; overflow-y: auto; }}
    #results.show {{ display: block; animation: fadeIn 0.3s; }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    .result-item {{ background: #f0fdf4; border: 2px solid #86efac; border-radius: 8px; padding: 0.8rem; margin-bottom: 0.6rem; font-size: 0.75rem; line-height: 1.4; }}
    .result-item strong {{ color: #15803d; font-size: 0.8rem; }}
    .result-item.info {{ background: #e0f2fe; border-color: #0284c7; }}
    .result-item.info strong {{ color: #0c4a6e; }}
    .loading {{ text-align: center; padding: 2rem; font-size: 1rem; color: #4a5568; }}
    .loading::after {{ content: '...'; animation: dots 1.5s steps(4, end) infinite; }}
    @keyframes dots {{ 0%, 20% {{ content: '.'; }} 40% {{ content: '..'; }} 60%, 100% {{ content: '...'; }} }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #f1f1f1; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb {{ background: #f59e0b; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #d97706; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1><span class="emoji">🤖</span> Predicción de Afluencia - Sistema IA</h1>
      <p>IFTS-12, A.Mercado, S.Paniagua, F.Hernández, A.Torchia</p>
    </header>
    <div class="nav-links">
      <a href="/">🏠 INICIO</a>
      <a href="/ui">📋 PANEL RECEPCIÓN</a>
      <a href="/vet/clinica/">🩺 ATENCIÓN CLÍNICA</a>
      <a href="/vet/gestion/">📊 GESTIÓN</a>
      <a href="/pets/view">🔍 MASCOTAS</a>
      <a href="/admin/api_docs_friendly">📚 API DOCS</a>
      <button class="btn-predict" onclick="predictAffluence()">🔮 REALIZAR PREDICCIÓN IA</button>
    </div>
    <div class="header-info">
      <div class="header-info-content">
        <div><strong>Sistema de IA</strong> que analiza el pronóstico del tiempo en <strong>Buenos Aires, Argentina</strong> para predecir la afluencia de clientes y el cumplimiento de turnos.</div>
        <div>Utiliza <strong>Machine Learning</strong> con datos históricos que correlacionan condiciones climáticas con asistencia a la veterinaria.</div>
        <div class="header-info-box"><strong>📍 Ubicación:</strong> Buenos Aires, ARG | <strong>📅 Fecha:</strong> <span id="currentDate">{fecha_formateada}</span> | <strong>📆 Semana:</strong> <span id="weekNumber">-</span></div>
      </div>
    </div>
    <div class="main-content">
      <div class="content-grid">
        <div class="left-column">
          <div class="card">
            <div class="card-header">🌤️ Clima Actual</div>
            <div class="card-body">
              <div class="current-data" id="weatherToday">
                <div class="data-item"><div class="icon">🌡️</div><div class="value">--°C</div><div class="label">Temperatura</div></div>
                <div class="data-item"><div class="icon">💧</div><div class="value">--%</div><div class="label">Humedad</div></div>
                <div class="data-item"><div class="icon">🌧️</div><div class="value">--%</div><div class="label">Prob. Lluvia</div></div>
                <div class="data-item"><div class="icon">💨</div><div class="value">-- km/h</div><div class="label">Viento</div></div>
              </div>
            </div>
          </div>
          <div class="card" style="flex: 1;">
            <div class="card-header">📅 Próximos 3 Días</div>
            <div class="card-body"><div class="forecast-mini" id="forecastMini"></div></div>
          </div>
        </div>
        <div class="right-column">
          <div class="card" style="flex: 1;">
            <div class="card-header">✨ Resultados de Predicción</div>
            <div class="card-body">
              <div id="results"><div id="resultsContent"></div></div>
              <div id="initialMessage" style="text-align: center; padding: 3rem; color: #9ca3af;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🤖</div>
                <p style="font-size: 1rem; font-weight: 600; color: #6b7280;">Presiona "Realizar Predicción IA" para analizar los datos climáticos y obtener el pronóstico de afluencia</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <script>
    function getWeekNumber() {{
      const now = new Date();
      const start = new Date(now.getFullYear(), 0, 1);
      const diff = now - start;
      const oneWeek = 1000 * 60 * 60 * 24 * 7;
      return Math.ceil(diff / oneWeek);
    }}
    function updateCurrentDate() {{
      document.getElementById('weekNumber').textContent = getWeekNumber();
    }}
    updateCurrentDate();
    function formatDate(dateStr) {{
      const date = new Date(dateStr);
      const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
      return days[date.getDay()] + ' ' + date.getDate() + '/' + (date.getMonth() + 1);
    }}
    async function loadWeatherData() {{
      try {{
        const response = await fetch('/ai/forecast?days=5');
        const data = await response.json();
        if (data.forecast && data.forecast.length > 0) {{
          const today = data.forecast[0];
          const weatherCards = document.querySelectorAll('#weatherToday .data-item .value');
          weatherCards[0].textContent = Math.round(today.temp_avg) + '°C';
          weatherCards[1].textContent = Math.round(today.humidity) + '%';
          weatherCards[2].textContent = Math.round(today.precipitation_probability) + '%';
          weatherCards[3].textContent = Math.round(today.windspeed_max) + ' km/h';
          const forecastMini = document.getElementById('forecastMini');
          forecastMini.innerHTML = '';
          data.forecast.slice(1, 4).forEach(day => {{
            const rainIcon = day.precipitation_probability > 50 ? '🌧️' : day.precipitation_probability > 30 ? '⛅' : '☀️';
            const dayCard = document.createElement('div');
            dayCard.className = 'forecast-mini-item';
            dayCard.innerHTML = '<div class="day">' + formatDate(day.date) + '</div><div class="temp">' + rainIcon + ' ' + Math.round(day.temp_avg) + '°C</div>';
            forecastMini.appendChild(dayCard);
          }});
        }}
      }} catch (error) {{
        console.error('Error cargando datos del clima:', error);
      }}
    }}
    if (document.readyState === 'loading') {{
      document.addEventListener('DOMContentLoaded', loadWeatherData);
    }} else {{
      loadWeatherData();
    }}
    async function predictAffluence() {{
      const resultsDiv = document.getElementById('results');
      const resultsContent = document.getElementById('resultsContent');
      const initialMessage = document.getElementById('initialMessage');
      initialMessage.style.display = 'none';
      resultsDiv.classList.add('show');
      resultsContent.innerHTML = '<div class="loading">Analizando datos climáticos y generando predicción</div>';
      try {{
        // Obtener fecha actual
        const today = new Date();
        const todayStr = today.toISOString().split('T')[0];
        
        const forecastResponse = await fetch('/ai/forecast?days=7');
        const forecastData = await forecastResponse.json();
        
        // Filtrar solo las fechas desde hoy en adelante
        const futureForecast = forecastData.forecast.filter(day => day.date >= todayStr);
        
        const predictions = [];
        for (const day of futureForecast.slice(0, 5)) {{
          const response = await fetch('/ai/predict?day=' + day.date);
          const predData = await response.json();
          predictions.push({{ date: day.date, weather: day, prediction: predData }});
        }}
        
        const hours = [9, 12, 15, 18];
        const noshowPromises = hours.map(hour => fetch('/ai/noshow?day=' + todayStr + '&hour=' + hour).then(r => r.json()));
        const noshowData = await Promise.all(noshowPromises);
        
        let html = '<div class="result-item"><strong>📊 Pronóstico de Afluencia de Clientes - Próximos 5 Días:</strong><br><br>';
        html += '<p style="margin-bottom: 0.8rem; font-size: 0.75rem;">El sistema analiza las condiciones del clima para estimar cuántos clientes visitarán la veterinaria cada día.</p>';
        
        predictions.forEach((pred, index) => {{
          const emoji = pred.prediction.label === 'Alta' ? '🟢' : pred.prediction.label === 'Media' ? '🟡' : '🔴';
          const prob = (pred.prediction.probability * 100).toFixed(0);
          const dateLabel = index === 0 ? '<strong style="color: #d97706;">HOY</strong>' : formatDate(pred.date);
          
          let interpretation = '';
          if (pred.prediction.label === 'Alta') {{
            interpretation = 'Se espera <strong>mucha afluencia</strong> de clientes';
          }} else if (pred.prediction.label === 'Media') {{
            interpretation = 'Se espera una <strong>cantidad normal</strong> de clientes';
          }} else {{
            interpretation = 'Se espera <strong>poca afluencia</strong> de clientes';
          }}
          
          html += emoji + ' ' + dateLabel + ': ' + interpretation + ' (confianza del ' + prob + '%) - Temperatura: ' + Math.round(pred.weather.temp_avg) + '°C, Probabilidad de lluvia: ' + Math.round(pred.weather.precipitation_probability) + '%<br>';
        }});
        
        html += '</div><div class="result-item"><strong>⏰ Pronóstico de Asistencia a Turnos de Hoy por Horario:</strong><br><br>';
        html += '<p style="margin-bottom: 0.8rem; font-size: 0.75rem;">Probabilidad de que los clientes con turno asistan o no asistan a su cita según el horario.</p>';
        
        noshowData.forEach(item => {{
          const prob = (item.probability * 100).toFixed(0);
          
          // Cambiar la lógica: si la probabilidad de "no show" es baja, significa alta asistencia
          let resultLabel, emoji, resultText;
          if (prob < 30) {{
            resultLabel = 'Alta Asistencia';
            emoji = '✅';
            resultText = 'Los clientes <strong>muy probablemente asistirán</strong> a sus turnos';
          }} else if (prob < 60) {{
            resultLabel = 'Asistencia Moderada';
            emoji = '⚠️';
            resultText = 'Algunos clientes <strong>podrían no asistir</strong>, se recomienda confirmar';
          }} else {{
            resultLabel = 'Alta Inasistencia';
            emoji = '❌';
            resultText = 'Muchos clientes <strong>probablemente no asistirán</strong>, confirmar turnos es prioritario';
          }}
          
          html += emoji + ' <strong>Turno de las ' + item.hour + ':00 hs</strong> - ' + resultText + ' (confianza del ' + prob + '%)<br>';
        }});
        
        const avgLabel = predictions[0].prediction.label;
        html += '</div><div class="result-item"><strong>💡 Recomendaciones Prácticas para Esta Semana:</strong><br><br>';
        if (avgLabel === 'Alta') {{
          html += '• <strong>Reforzar el equipo:</strong> Contar con más personal disponible para atender la demanda<br>';
          html += '• <strong>Revisar inventario:</strong> Verificar que haya suficientes medicamentos, vacunas y materiales<br>';
          html += '• <strong>Extender horarios:</strong> Considerar ampliar los horarios de atención si es posible<br>';
          html += '• <strong>Clima favorable:</strong> Las buenas condiciones climáticas favorecen la asistencia';
        }} else if (avgLabel === 'Media') {{
          html += '• <strong>Personal habitual:</strong> Mantener la dotación de personal normal<br>';
          html += '• <strong>Recordatorios:</strong> Enviar mensajes de confirmación de turnos a los clientes<br>';
          html += '• <strong>Stock regular:</strong> Mantener los niveles habituales de insumos y medicamentos<br>';
          html += '• <strong>Clima moderado:</strong> Las condiciones climáticas no deberían afectar significativamente';
        }} else {{
          html += '• <strong>Reprogramar turnos:</strong> Considerar llamar a los clientes para confirmar o reprogramar citas<br>';
          html += '• <strong>Confirmar asistencias:</strong> Es muy importante contactar a los clientes con turno programado<br>';
          html += '• <strong>Tiempo administrativo:</strong> Aprovechar para organizar archivos, actualizar fichas o capacitación<br>';
          html += '• <strong>Clima adverso:</strong> Las malas condiciones climáticas pueden desalentar la asistencia';
        }}
        html += '</div><div class="result-item info"><strong>🌐 Fuente de la Información:</strong><br><br>';
        html += 'Los datos del clima provienen de <strong>Open-Meteo</strong>, un servicio meteorológico profesional para Buenos Aires, Argentina.<br>';
        html += 'Las predicciones se calculan con <strong>Inteligencia Artificial</strong> entrenada con datos históricos de la veterinaria.<br>';
        html += '<strong>Fecha y hora del análisis:</strong> ' + new Date().toLocaleString('es-AR') + '</div>';
        resultsContent.innerHTML = html;
      }} catch (error) {{
        resultsContent.innerHTML = '<div class="result-item" style="background: #fee2e2; border: 2px solid #ef4444;"><strong style="color: #991b1b;">❌ Error al realizar predicción</strong><br><br>' + error.message + '<br><br>Detalles: Hubo un problema al obtener los datos meteorológicos o realizar la predicción. Por favor, verifica la conexión a internet y que los modelos de IA estén entrenados.</div>';
      }}
    }}
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
