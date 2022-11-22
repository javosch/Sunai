import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


folder = r'C:\Users\JavierSchmitt\Documents\Python Scripts\Sunai'
files = os.listdir(folder)
files = [file for file in files if os.path.isfile(file) and file[-4:] == 'xlsx']

df = pd.DataFrame()

file_chart = 'line_cart.png'

for file in files:
    path_temp = os.path.join(folder, file)
    df_temp = pd.read_excel(path_temp)
    df = pd.concat([df, df_temp])

    # Resetear variable para ahorrar memoria
    df_temp = '0'

df.fecha_im = pd.to_datetime(df.fecha_im)
df.fecha_recepcion_inversor_medicion = pd.to_datetime(df.fecha_recepcion_inversor_medicion)

# Pasar a tipo numerico y tomar los valores no numericos como nulos
df.active_power_im = pd.to_numeric(df.active_power_im, errors='coerce')

x_axis = df.fecha_im
y_axis = df.active_power_im

plt.plot(x_axis, y_axis)
plt.title('title name')
plt.xlabel('Date')
plt.ylabel('Active Power')
plt.title('Active Power by Date')
plt.savefig(file_chart)

suma_active_power = df.groupby(df.fecha_im.dt.day).active_power_im.sum().values
suma_dia_active_power = df.groupby(df.fecha_im.dt.day).active_power_im.sum().index.values

min_active_energy = df.active_energy_im.min()
max_active_energy = df.active_energy_im.max()

path_chart = os.path.join(folder, file_chart)

file_txt = r'respuestas.txt'
path_txt = os.path.join(folder, file_txt)

if os.path.exists(path_txt):
    os.remove(path_txt)

with open(path_txt, 'w+') as txt:
    txt.write('Respuestas:')
    for i in range(len(suma_dia_active_power)):
        txt.write(f'\nSuma Active Power para el dia {suma_dia_active_power[i]} fue de {suma_active_power[i]}')
    txt.write(f'\nValor mínimo de Active Energy es de {min_active_energy}')
    txt.write(f'\nValor máximo de Active Energy es de {max_active_energy}')
    txt.write(f'\nRuta al gráfico de linea {path_chart}')
    txt.close()

# Suponiendo que id_p es el ID por planta
for i in range(len(suma_dia_active_power)):
    print(f'\nSuma Active Power para el dia {suma_dia_active_power[i]} fue de {suma_active_power[i]}')

suma_active_power_planta = df.groupby([df.fecha_im.dt.day, df.id_p]).active_power_im.sum().values
suma_dia_active_power_planta = df.groupby([df.fecha_im.dt.day, df.id_p]).active_power_im.sum().index.values
for i in range(len(suma_active_power_planta)):
    print(f'\nSuma Active Power para la planta {suma_dia_active_power_planta[i][1]} dia {suma_dia_active_power_planta[i][0]} fue de {suma_active_power_planta[i]}')

print('ok')