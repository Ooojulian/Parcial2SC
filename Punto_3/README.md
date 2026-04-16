# Punto 3: Net Interactions - Dinámicas Acopladas

## ¿Qué es el Punto?

Implementar **Net Interactions** usando **programación funcional pura**.

Define cómo múltiples elementos se afectan mutuamente simultáneamente via:
- **Matriz de pesos W**: quién influye en quién
- **Función de activación F**: cómo responde cada elemento
- **Evolución dinámica**: x_{n+1} = W @ F(x_n)

---

## Objetivos

Demostrar que programación funcional define bien el concepto de "interacción":

1. ✓ Descomposición funcional (activate, weight, aggregate)
2. ✓ Composición de funciones (pipeline puro)
3. ✓ Dinámicas acopladas (iteración hasta convergencia)
4. ✓ Convergencia a puntos fijos (x* = W @ F(x*))
5. ✓ Análisis de estabilidad (eigenvalores < 1)

---

## Cómo Ejecutar

**Ver la respuesta:**
```bash
cat SOLUCION.md
```

**Entender conceptos:**
```bash
cat CONCEPTOS.md
```

**Ver el código:**
```bash
cat src/net_interactions.py
```

**Ejecutar programa:**
```bash
python main.py
```

**Validar (26 tests):**
```bash
pytest tests/ -q
```
