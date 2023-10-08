from queue import Queue
from agente import Agente
import manager as mn
from graphviz import Digraph

mapa = [
    ['', 'uta', '', '', ''],
    ['', '', '', '', ''],
    ['', '', 'mall', '', ''],
    ['', '', '', '', ''],
    ['', '', '', '', ''],
]


puntoInicial = mn.obtenerUbicacion('uta', mapa)
puntoObjetivo = mn.obtenerUbicacion('mall', mapa)
print(f'UTA {puntoInicial}')
print(f'MALL {puntoObjetivo}')

raiz = Agente()
raiz.inicio(mapa, puntoInicial, puntoObjetivo)
raiz.controlarRepetidos = True #activo el control de los repetidos

grafo = Digraph()
pila = []
pila.append(raiz)

solucion:Agente = None
profundidad_maxima = 1
profundidad_actual = 0
ultimos_agregados = []
print('buscando solucion ...')
while True:
    if len(pila) <= 0:
        pila.extend(ultimos_agregados)
        profundidad_maxima += 1
        
    estadoActual:Agente = pila.pop()
    grafo.node(estadoActual.obtenerID(), estadoActual.obtenerID())
    if estadoActual.esObjetivo(): # control si es objetivo
        solucion = estadoActual
        grafo.node(estadoActual.obtenerID(), estadoActual.obtenerID())
        print('solucion encontrada ...')
        break
    
    if estadoActual.nivel >= profundidad_maxima:
        continue
    
    nuevosEstados = mn.ejecutarMovimientos(mn.generarHijos(estadoActual, 4))
    ultimos_agregados.clear()
    ultimos_agregados.extend(nuevosEstados)
    for nuevo in nuevosEstados:
        grafo.node(nuevo.obtenerID(), nuevo.obtenerID())
        grafo.edge(estadoActual.obtenerID(), nuevo.obtenerID())
        pila.append(nuevo)
    profundidad_actual += 1
    
    
        
mapaVacio = mn.dibujarMapaVacio(len(mapa), len(mapa[0]))
mn.dibujarRutaSolucion(solucion, mapaVacio)
solucion.mostrarcaminoRecorrido()
grafo.render("arbol_busqueda", view=True)
