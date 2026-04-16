# Punto 1: Internet Topology - Redes Scale-Free

## ¿Qué es el Punto?

Explicar la **complejidad de Internet** mediante modelo matemático: ¿Por qué es robusta a fallos pero frágil a ataques? ¿Cómo creció sin diseño centralizado?

## Respuesta

Internet es **red scale-free** (ley de potencia P(k) ∼ k^{-γ}):
- Emerge de **apego preferencial** (nodos nuevos conectan proporcional a grado)
- Genera **hubs gigantes** (eficientes pero vulnerables)
- Resultado: Pequeño mundo, robusta a ruido, frágil a ataques

## Modelo

**Barabási-Albert:** Generativo que produce ley de potencia observada en Internet real

## Cómo Ejecutar

**Ver la respuesta (por qué Internet es compleja):**
```bash
cat SOLUCION.md
```

**Entender conceptos:**
```bash
cat CONCEPTOS.md
```

**Ver topología y análisis:**
```bash
python main.py
```

**Validar (28 tests):**
```bash
pytest tests/ -q
```
