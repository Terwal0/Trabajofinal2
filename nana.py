@app.route('/', methods=['GET', 'POST'])  #Modelo para obtener y entregar
def index():
  if request.method == 'POST':  #Tipo de modelo
    try:
      G = float(request.form['G'])  #Pide el valor de G
      T = float(request.form['T'])  #Pide el valor de T
      pv_model = PVModel()  #Se llama el modelo anterior
      Vmp, Imp, Pmax = pv_model.modelo_pv(G, T)  #Se evalúa
      result = f'Vmp = {Vmp:.2f} V, Imp = {Imp:.2f} A, Pmax = {Pmax:.2f} W'  #Se guarda el resultado en una cadena de texto
    except ValueError as e:
      result = f'Error: Entrada no válida. {e}'
    except Exception as e:
      result = f'Error en el cálculo: {e}'  #Captura posibles errores
    return render_template_string(
        '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Resultado del Modelo Fotovoltaico</title>
            </head>
            <body>
                <h1>Resultado del Modelo Fotovoltaico</h1>
                <p>{{ result }}</p>
                <a href="/">Intentar de nuevo</a>
            </body>
            </html>
        ''',
        result=result)  #Muestra en la página que hay un error
  else:
    return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Simulador de Panel Fotovoltaico</title>
            </head>
            <body>
                <h1>Simulador de Panel Fotovoltaico</h1>
                <form method="post">
                    Irradiancia (G) en W/m²: <input type="text" name="G" required><br>
                    Temperatura (T) en °C: <input type="text" name="T" required><br>
                    <input type="submit" value="Calcular">
                </form>
            </body>
            </html>
        ''')  #Muestra el resultado en la pantalla
