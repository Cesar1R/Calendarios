import csv
import matplotlib.pyplot as plt

def graficar_desde_csv(ruta_archivo):
    # Lista para almacenar los arreglos
    arreglos = []

    # Abre el archivo CSV en modo lectura ('r')
    with open(ruta_archivo, 'r') as csvfile:
        # Crea un objeto lector CSV
        lector_csv = csv.reader(csvfile)

        # Itera sobre las filas del archivo CSV
        for fila in lector_csv:
            # Convierte los elementos de la fila a números y agrega el arreglo a la lista
            arreglo = [float(dato) for dato in fila]
            arreglos.append(arreglo)

    # Nombres de los meses
    meses = [str(i) for i in range(1, 13)]

    # Colores y etiquetas para los arreglos
    colores = ['r', 'g', 'b', 'c', 'm', 'y', 'k', '#FFA500', '#00FF00', '#800080', '#FF00FF', '#008080']
    etiquetas = ["Dr. Covarrubias Mata", "Terapias", "Dr. Covarrubias Arroyo"]
    #etiquetas = [f'Arreglo {i+1}' for i in range(len(arreglos))]

    # Grafica los datos
    for i in range(len(arreglos)):
        plt.plot(meses, arreglos[i], label=etiquetas[i], color=colores[i], marker='o')
        for j, valor in enumerate(arreglos[i]):
            plt.text(j  , valor,f'{int(valor)}', ha='center', va='bottom', fontsize=10)
    # Configuraciones del gráfico
    plt.xlabel('Meses de 2023')
    plt.ylabel('Datos Numéricos')
    plt.title('Gráfico de Datos Numéricos por Mes')
    plt.legend()
    plt.grid(True)

    # Muestra la gráfica
    plt.show()

# Ruta del archivo CSV
archivo_csv = "---------------------------------"

# Llama a la función para graficar
graficar_desde_csv(archivo_csv)
