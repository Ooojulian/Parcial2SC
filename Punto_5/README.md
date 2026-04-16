# Punto 5: Attractors - Modelado Basado en Agentes

## ¿Qué es el Punto?

Explicar el **concepto de atractor en sistemas complejos** usando **modelamiento basado en agentes (ABM)**.

## Pregunta Central

**¿Se explica el concepto de atractor con ABM?**

## Respuesta

**SÍ:** Simular 30 agentes independientes con reglas locales idénticas demuestra que todas sus órbitas **convergen al MISMO atractor sin coordinación explícita**.

Esto revela que atractores son propiedades emergentes de sistemas dinámicos, no conceptos abstractos.

## Los 3 Atractores (ABM demuestra cada uno)

1. **Punto Fijo:** 30 agentes con x_{n+1}=r·x_n(1-x_n) → todos convergen a x*=0.6429
2. **Ciclo Límite:** 30 agentes con φ_{n+1}=φ_n+ω (mod 2π) → todos en período T=12
3. **Caos (Lorenz):** 30 agentes integrando Lorenz → todos en mariposa de Lorenz (dimensión fractal 2.06)

## Cómo Ejecutar

**Ver la respuesta (cómo ABM explica atractores):**
```bash
cat SOLUCION.md
```

**Entender conceptos:**
```bash
cat CONCEPTOS.md
```

**Ver emergencia de atractores en acción:**
```bash
python main.py
```

**Validar (36 tests):**
```bash
pytest tests/ -q
```
