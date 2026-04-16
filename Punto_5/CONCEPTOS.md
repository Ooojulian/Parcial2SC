# Conceptos Clave - Punto 5: Atractores

**Para conceptos generales (punto fijo, órbita periódica, eigenvalores, caos, etc.), ver CONCEPTOS_GENERALES.md en la raíz.**

---

## 1. Los 3 Atractores de Punto 5

### Atractor 1: Punto Fijo (Fixed Point)

**Sistema:** x_{n+1} = r·x_n(1 - x_n) con r = 2.8

**Propiedades:**
- Dimensión = 0 (un punto)
- Convergencia exponencial desde cualquier x₀
- Punto fijo teórico: x* = 1 - 1/r

**Ejemplo (r = 2.8):**
```
x₀ = 0.5
x₁ = 2.8 × 0.5 × 0.5 = 0.7
x₂ = 2.8 × 0.7 × 0.3 = 0.588
...
x∞ = 1 - 1/2.8 ≈ 0.6429 ← punto fijo
```

**Interpretación en ABM:**
- 30 agentes, cada uno evoluciona independientemente
- Todos convergen al mismo x* aunque empiezan diferente
- Ejemplo natural: temperatura aumenta lentamente → equilibrio térmico

---

### Atractor 2: Ciclo Límite (Limit Cycle)

**Sistema:** φ_{n+1} = φ_n + ω (mod 2π)

Oscilador de fase con período T = 2π/ω

**Propiedades:**
- Dimensión = 1 (curva cerrada, típicamente círculo)
- Período T = 12 pasos en Punto 5
- Todas las órbitas convergen al ciclo (sincronización)
- Aislado: perturbaciones pequeñas no destroyen el ciclo

**Ejemplo (T = 12, ω ≈ 0.524):**
```
φ₀ = 0.0
φ₁ = 0.524
φ₂ = 1.048
...
φ₁₂ = 6.283 ≈ 0 (mod 2π) ← retorna al inicio
```

**Interpretación en ABM:**
- 30 agentes oscilan periódicamente
- Todas las fases están acopladas por ω
- Ejemplo natural: corazón latiendo, neuronas disparando rítmicamente

---

### Atractor 3: Atractor Extraño (Strange Attractor - Lorenz)

**Sistema:** 3 ecuaciones diferenciales acopladas

```
dx/dt = σ(y - x)
dy/dt = x(ρ - z) - y
dz/dt = xy - βz
```

**Parámetros (régimen caótico):**
- σ = 10 (número de Prandtl)
- ρ = 28 (número de Rayleigh)
- β = 8/3 (razón geométrica)

**Propiedades:**
- Dimensión fractal ≈ 2.06 (entre 2D y 3D)
- Caótico: λ_Lyapunov > 0, sensible a CI
- Determinista pero impredecible (~50 pasos máximo)
- Visual: dos "alas de mariposa" danzando

**En ABM:**
- 30 agentes integran Lorenz con Runge-Kutta
- Todos convergen a la misma región (atractor)
- Pero cada uno sigue trayectoria ligeramente diferente (caos)

---

## 2. Dimensión Fractal del Atractor

### Dimensión de Correlación

Mide la dimensión efectiva del atractor analizando cómo cambia el número de pares de puntos cercanos:

$$C(r) \sim r^{D_c}$$

Donde r es distancia y C(r) es número de pares dentro de distancia r.

### Valores Típicos

| Atractor | Dimensión | Tipo |
|----------|-----------|------|
| Punto fijo | 0 | Cero-dimensional |
| Ciclo límite | 1 | Unidimensional (curva) |
| Toro | 2 | Bidimensional |
| Lorenz | 2.06 | Fractal (entre 2D y 3D) |

### Interpretación

**D_c = 2.06 para Lorenz significa:**
- Más complejo que una superficie (2D)
- Menos complejo que un volumen (3D)
- Estructura autosimilar a múltiples escalas

---

## 3. Sistema de Lorenz

### Origen Histórico

Lorenz (1963) simplificó ecuaciones de convección atmosférica para estudiar predictibilidad del clima.

### Ecuaciones Simplificadas

```
dx/dt = σ(y - x)        [difusión térmica]
dy/dt = x(ρ - z) - y    [flotabilidad vs disipación]
dz/dt = xy - βz         [retroalimentación]
```

### Regímenes por ρ

| ρ | Comportamiento |
|---|---|
| ρ < 1 | Punto fijo estable en origen |
| 1 < ρ < 24.74 | Punto fijo único (estable) |
| ρ = 24.74 | Bifurcación Hopf |
| 24.74 < ρ < 28 | Ciclo límite (órbita periódica) |
| ρ ≥ 28 | Caos (atractor extraño) |

### Integración Numérica

**Método:** Runge-Kutta 4to orden (RK4)

```
dt = 0.01 (tamaño paso)
1500 pasos → 15 segundos de tiempo simulado
```

Ventaja: Error O(dt^5), muy preciso para dinámicas caóticas.

---

## 4. Modelado Basado en Agentes (ABM)

### Arquitectura

Cada agente es entidad autónoma:

```
Para cada paso temporal:
    Para cada agente:
        1. Observar estado actual x_n
        2. Aplicar dinámica local: x_{n+1} = f(x_n; parámetros)
        3. Actualizar posición
```

### Ventaja para Punto 5

- Múltiples agentes permiten ver **sincronización global**
- Todos convergen al atractor sin coordinación explícita
- Demuestra que orden global emerge de reglas locales

---

## 5. Convergencia y Sincronización

### Convergencia (Convergence)

Trayectorias se estabilizan en región acotada.

**Métricas:**
- Distancia máxima al atractor
- Varianza de trayectorias
- Número de pasos para "settle"

### Sincronización (Synchronization)

Múltiples agentes alineados en el mismo atractor.

**Para punto fijo:** Todos alcanzan x* ≈ 0.6429

**Para ciclo límite:** Todas las fases alineadas (período T = 12)

**Para Lorenz:** Todos exploran misma región mariposa, pero no en sincronía exacta (caos)

---

## 6. Diccionario Punto 5

| Término | Definición | Símbolo |
|---------|-----------|---------|
| **Atractor** | Conjunto que atrae órbitas cercanas | A |
| **Punto fijo** | f(x*) = x*, equilibrio | x* |
| **Ciclo límite** | Órbita periódica aislada | T |
| **Atractor extraño** | Fractal con caos | - |
| **Dimensión fractal** | Dimensión no-entera | D_c |
| **Lorenz** | Sistema de 3 ODEs caóticas | σ, ρ, β |
| **Sincronización** | Múltiples agentes convergen al atractor | - |
| **Convergencia** | Trayectorias se estabilizan | ε |
| **Runge-Kutta RK4** | Integrador numérico preciso | dt |
| **Condición inicial** | Estado inicial x₀ | x₀ |
| **Lyapunov exponent** | Divergencia exponencial (ver CONCEPTOS_GENERALES.md) | λ |
| **Bifurcación Hopf** | Punto fijo → ciclo límite | ρ = 24.74 |

---

**Para más detalles sobre atractores, bifurcaciones, caos y dinámicas, ver CONCEPTOS_GENERALES.md**
