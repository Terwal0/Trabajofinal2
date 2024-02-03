from flask import Flask, request, render_template_string
import numpy as np
from scipy.optimize import fsolve
import time

app = Flask(__name__)


class PVModel:

  def __init__(self, num_panels_series=1, num_panels_parallel=1):
    self.R_sh = 545.82  # Resistencia en paralelo [Ohm]
    self.k_i = 0.037  # Coeficiente de temperatura para la corriente de cortocircuito [A/K]
    self.T_n = 298  # Temperatura de referencia [K]
    self.q = 1.60217646e-19  # Carga del electrón [C]
    self.n = 1.0  # Factor de idealidad
    self.K = 1.3806503e-23  # Constante de Boltzmann [J/K]
    self.E_g0 = 1.1  # Energía de banda prohibida [eV]
    self.R_s = 0.39  # Resistencia en serie [Ohm]
    self.I_sc = 9.35 * num_panels_parallel  # Corriente de cortocircuito [A]
    self.V_oc = 47.4 * num_panels_series  # Voltaje de circuito abierto [V]
    self.N_s = 72 * num_panels_series  # Número de células en serie

  def validate_inputs(self, G, T):
    """
        Validar los valores de irradiancia y temperatura.
        :param G:  Irradiancia (W/m²)
        :param T:  Temperatura (K)
        :return:  None
        """
    if not isinstance(G, (int, float)) or G <= 0:
      raise ValueError("La irradiancia (G) debe ser un número positivo.")
    if not isinstance(T, (int, float)) or T <= 0:
      raise ValueError("La temperatura (T) debe ser un número positivo.")
    if not isinstance(self.num_panels_series,
                      int) or self.num_panels_series <= 0:
      raise ValueError(
          "El número de paneles en serie debe ser un entero positivo.")
    if not isinstance(self.num_panels_parallel,
                      int) or self.num_panels_parallel <= 0:
      raise ValueError(
          "El número de paneles en paralelo debe ser un entero positivo.")

  def modelo_pv(self, G, T):
    T += 273.15  # Convertir de Celsius a Kelvin
    I_rs = self.I_sc / (np.exp(
        (self.q * self.V_oc) / (self.n * self.N_s * self.K * T)) - 1)
    I_o = I_rs * (T / self.T_n)**3 * np.exp(
        (self.q * self.E_g0 * (1 / self.T_n - 1 / T)) / (self.n * self.K))
    I_ph = (self.I_sc + self.k_i * (T - self.T_n)) * (G / 1000)
    Vpv = np.linspace(0, self.V_oc, 1000)

    def diode_eq(I, V):
      return I_ph - I_o * (np.exp(
          (self.q * (V + I * self.R_s)) /
          (self.n * self.K * T)) - 1) - (V + I * self.R_s) / self.R_sh - I

    Ipv = fsolve(diode_eq, self.I_sc * np.ones_like(Vpv), args=(Vpv))
    Ppv = Vpv * Ipv
    max_power_idx = np.argmax(Ppv)
    return Vpv[max_power_idx], Ipv[max_power_idx], Ppv[max_power_idx]


app = Flask(__name__)


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


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=False)
  print("La aplicación está en ejecución. Presiona Ctrl+C para detenerla.")
  time.sleep(5)  # Espera 5 segundos antes de salir
