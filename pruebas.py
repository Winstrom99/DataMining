import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from gsppy.gsp import GSP

# Cargar el archivo CSV
file_path = "/mnt/data/Navegacion_Web.csv"
df = pd.read_csv(file_path)

# Convertir Timestamp a formato datetime y ordenar por usuario y tiempo
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df = df.sort_values(by=['UserID', 'Timestamp'])

# Agrupar por usuario y obtener la secuencia de acciones
sequences = df.groupby('UserID')['Action'].apply(list).tolist()

# Función para aplicar GSP con diferentes valores de soporte
def aplicar_gsp(sequences, min_support):
    gsp = GSP(min_support=min_support)
    patterns = gsp.fit(sequences)
    return patterns

# Probar con diferentes valores de soporte
supports = [0.05, 0.1, 0.2]
patterns_dict = {}
for sup in supports:
    patterns_dict[sup] = aplicar_gsp(sequences, sup)
    print(f"Patrones con soporte {sup}:", patterns_dict[sup])

# Visualizar la distribución de acciones en la web
actions = [action for seq in sequences for action in seq]  # Extraer todas las acciones
counts = Counter(actions)

plt.figure(figsize=(8,5))
plt.bar(counts.keys(), counts.values())
plt.xlabel("Acciones en la Web")
plt.ylabel("Frecuencia")
plt.title("Distribución de Acciones en la Web")
plt.xticks(rotation=45)
plt.show()

# Eliminar una transacción clave y analizar cambios
df_filtered = df[df['Action'] != 'Purchase']  # Ejemplo: eliminar compras
sequences_filtered = df_filtered.groupby('UserID')['Action'].apply(list).tolist()
patterns_filtered = aplicar_gsp(sequences_filtered, 0.1)

print("Patrones después de eliminar la acción 'Purchase':", patterns_filtered)
