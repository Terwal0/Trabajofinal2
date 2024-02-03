Autores: Raul Velez, Walter Garzón G.

Introducción: El siguiente programa tiene como finalidad presentar los resultados de un simulador Fotovoltaico. Este se compone de dos botones en los cuales se ingresa la irradiancia y la temperatura en un ambiente controlado y se presenta la máxima potencia en wats que
se obtiene con esos valores.

Este se modelo se obtiene a partir de un trabajo investigativo en el cual se presentan las siguientes variables:
-  R_sh = Resistencia en paralelo [Ohm]
-  k_i = Coeficiente de temperatura para la corriente de cortocircuito [A/K]
-  T_n = Temperatura de referencia [K]
-  q = Carga del electrón [C]
-  n = 1.0 Factor de idealidad
-  K = Constante de Boltzmann [J/K]
-  E_g0 = Energía de banda prohibida [eV]
-  R_s = Resistencia en serie [Ohm]
-  I_sc = Corriente de cortocircuito [A]
-  V_oc = Voltaje de circuito abierto [V]
-  N_s = Número de células en serie

Estas constantes se ingresan en Python y la idea principal es analizar el comportamiento de los valores máximos de potencia cuando varia la temperatura y la irradiancia. Además, se construye un código el cual crea una página en HTML para realizar la interacción mencionada
anteriormente y que da la posibilidad y comodidad de analizar con más facilidad de compartir los datos obtenidos.
