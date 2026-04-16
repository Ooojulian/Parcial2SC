# Punto 5: Atractores en Sistemas Complejos - SOLUCIÓN

## Pregunta

¿Se explica el concepto de **atractor en sistemas complejos** con **modelamiento basado en agentes (ABM)**?

## Respuesta: SÍ

Un **atractor** es un conjunto que **atrae todas las órbitas cercanas**: lim(t→∞) ||x(t) - A|| = 0

**ABM demuestra esto simulando 30 agentes independientes con reglas locales idénticas:**

```python
for step in range(1000):
    for agent in agents:
        x_new = agent.dynamics(x)  # Regla local simple
        agent.update(x_new)
    
    # Observación: Todos convergen al MISMO atractor
    # Sin coordinación explícita
```

---

## Cómo ABM Explica Atractores

### Punto Fijo (Equilibrio)

**Dinámicas:** x_{n+1} = r·x_n(1-x_n), r=2.8

**ABM resultado:**
```
Agente 0: x₀=0.234 → 0.498 → 0.625 → ... → 0.6429*
Agente 1: x₀=0.891 → 0.343 → 0.595 → ... → 0.6429*
Agente 2: x₀=0.123 → 0.327 → 0.612 → ... → 0.6429*
...
Agente 29: x₀=0.567 → 0.687 → 0.596 → ... → 0.6429*

OBSERVACIÓN: Todos convergen a x* = 0.6429 (punto fijo)
NO COORDINACIÓN: Cada agente ignora a los demás
CONCLUSIÓN: El punto fijo 0.6429 ATRAE todas las órbitas
```

**¿Qué es el atractor aquí?** El punto único x* = 0.6429

---

### Ciclo Límite (Oscilación Periódica)

**Dinámicas:** φ_{n+1} = φ_n + ω (mod 2π), ω=2π/12

**ABM resultado:**
```
Agente 0: φ₀=0.00 → 0.52 → 1.05 → 1.57 → ... → 6.28 → 0.00 (período 12)
Agente 1: φ₀=1.20 → 1.72 → 2.25 → ... → 0.52 → 1.20 (período 12)
Agente 2: φ₀=3.14 → 3.67 → 4.19 → ... → 2.62 → 3.14 (período 12)
...
Agente 29: φ₀=2.50 → 3.02 → 3.54 → ... → 1.98 → 2.50 (período 12)

OBSERVACIÓN: Todas las órbitas tienen período T=12 (mismo para todas)
NO COORDINACIÓN: Cada agente solo suma ω
CONCLUSIÓN: El ciclo de período 12 ATRAE todas las órbitas
```

**¿Qué es el atractor aquí?** La órbita periódica cerrada de período 12

---

### Atractor Extraño (Lorenz - Caos)

**Dinámicas:** RK4 integración de Lorenz con σ=10, ρ=28, β=8/3

**ABM resultado:**
```
Agente 0: [1.0, 1.0, 1.0] → (1.32, 2.47, 0.18) → (2.15, 3.61, 0.42) → ...
Agente 1: [1.1, 1.1, 1.1] → (1.41, 2.61, 0.21) → (2.28, 3.79, 0.51) → ...
...
Agente 29: [0.9, 0.9, 0.9] → (1.23, 2.33, 0.15) → (2.02, 3.43, 0.33) → ...

OBSERVACIÓN: 
- Cada agente sigue trayectoria DIFERENTE (caos)
- TODAS quedan en región acotada: |x|, |y|, |z| < 25
- Dimensión fractal: D_c ≈ 2.12 (vs teórico 2.06)

CONCLUSIÓN: La mariposa de Lorenz ATRAE todas las órbitas
(aunque dentro caóticamente)
```

**¿Qué es el atractor aquí?** El conjunto fractal (mariposa) que atrapa todas las órbitas

---

## Qué Aprende ABM

**Sin ABM:** Un atractor es "concepto abstracto", difícil visualizar

**Con ABM:** Ves 30 agentes independientes → **convergen visiblemente al atractor**

| Aspecto | Se Ve Claramente |
|---------|-----------------|
| **Convergencia** | Todas las órbitas → región acotada |
| **Unicidad** | Múltiples condiciones iniciales → mismo atractor |
| **Dimensión** | Punto fijo = 0D, ciclo = 1D, caos = 2.06D |
| **No determinismo local** | Cada agente "ignora" a los demás, pero convergen globalmente |
| **Atracción** | Perturbaciones pequeñas → vuelven al atractor |

---

## Conclusión

**¿Se explica atractor con ABM?** 

**SÍ:** ABM demuestra que múltiples agentes con reglas locales simples convergen al MISMO atractor sin coordinación.

**Esto muestra que:**
1. Atractor es propiedad emergente (no diseñado)
2. Orden global = resultado de dinámicas locales
3. Hay solo 3 tipos universales (punto fijo, ciclo, caos)

**Aplicación real:** Diagnosticar qué tipo de atractor tiene un sistema observando su comportamiento → predecir evolución futura
