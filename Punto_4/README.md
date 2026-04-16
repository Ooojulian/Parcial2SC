# Punto 4: Feigenbaum Delta - Universalidad en Bifurcaciones

## ¿Qué es el Punto?

Usando **universalidad (δ) como constante de la naturaleza**, explicar desde un modelo computacional cómo se puede usar δ para **resolver un problema de ingeniería**.

## Problema de Ingeniería

**Caso:** Sistema dinámico (población, circuito, fluido) con parámetro r que varía.

**¿Cuándo pasa a comportamiento caótico?**

- Sin δ: Analizar cada sistema (tedioso)
- Con δ: **Predicción universal**, mismo δ para todos los sistemas

## Modelo Computacional

**Mapa Logístico:** x_{n+1} = r·x_n(1-x_n)

¿Por qué?
- Sistemas reales tienen dinámicas unimodales
- Bifurcación período-doble es universal
- Computacionalmente simple

## Solución

1. Detectar bifurcaciones (período 1→2→4→8→caos)
2. Calcular δ ≈ 4.6692 (converge)
3. Predecir onset caos: r_∞ ≈ r_n + (r_n - r_{n-1}) / δ

**Conclusión:** δ permite predecir cuándo sistema colapsa, sin medir δ en cada sistema específico (universalidad)

## Cómo Ejecutar

**Ver la respuesta (cómo δ resuelve el problema):**
```bash
cat SOLUCION.md
```

**Entender conceptos:**
```bash
cat CONCEPTOS.md
```

**Ver bifurcaciones en acción:**
```bash
python main.py
```

**Validar (37 tests):**
```bash
pytest tests/ -q
```
