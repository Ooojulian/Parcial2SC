# Conceptos Clave - Punto 4: Constante de Feigenbaum δ

**Para conceptos generales (bifurcación, eigenvalores, Lyapunov, etc.), ver CONCEPTOS_GENERALES.md en la raíz.**

---

## 1. ¿Qué es la Constante de Feigenbaum δ?

### Definición Formal

$$\delta = \lim_{n \to \infty} \frac{r_n - r_{n-1}}{r_{n+1} - r_n} \approx 4.66920160910...$$

Donde r_n es el parámetro donde ocurre la n-ésima bifurcación período-doble.

### Intuición

Número que describe **qué tan rápido** un sistema bifurca hacia caos. Mide la velocidad de duplicación de período conforme aumenta un parámetro.

### Analogía

Instrumento que suena en nota A, luego alterna A-B, luego A-B-C-D, luego 8 notas, luego infinitas (ruido). δ controla qué tan rápido acelera esa cascada.

---

## 2. Mapa Logístico (Sistema Usado)

### Ecuación

$$x_{n+1} = r \cdot x_n \cdot (1 - x_n)$$

Rango: x ∈ [0, 1], r ∈ [0, 4]

### Regímenes por Valor de r

| r | Comportamiento | Atractor |
|---|---|---|
| r < 1 | Colapso a 0 | x* = 0 |
| 1 < r < 3 | Converge a punto fijo | x* = 1 - 1/r |
| r = 3 | Primera bifurcación | Transición |
| 3 < r < 3.449 | Período-2 estable | {A, B} |
| r ≈ 3.449 | Segunda bifurcación | Transición |
| 3.449 < r < 3.544 | Período-4 | {A,B,C,D} |
| r ≈ 3.5699 | Infinitas bifurcaciones | Onset caos |
| 3.57 < r < 4 | **Caos** (con ventanas) | Fractal + islas |
| r = 4 | Caos máximo | Atractor Lorenz 1D |

### Punto Fijo Analítico

Estable si |f'(x*)| < 1:

```
f'(x) = r(1-2x)
En punto fijo: f'(x*) = 2-r

Estable si: |2-r| < 1
⟹ 1 < r < 3
```

---

## 3. Cascada Período-Doble (Cómo Se Calcula δ)

### Bifurcaciones Observadas

```
r₁ ≈ 3.000    (período 1 → período 2)
r₂ ≈ 3.449    (período 2 → período 4)
r₃ ≈ 3.544    (período 4 → período 8)
r₄ ≈ 3.5687   (período 8 → período 16)
...
r∞ ≈ 3.5699   (infinitas bifurcaciones)
```

### Cálculo de δ

```
Espaciamiento entre bifurcaciones:
Δ₁ = r₂ - r₁ = 3.449 - 3.000 = 0.449
Δ₂ = r₃ - r₂ = 3.544 - 3.449 = 0.095
Δ₃ = r₄ - r₃ = 3.5687 - 3.544 = 0.0247

Ratio:
δ₁ = Δ₁ / Δ₂ = 0.449 / 0.095 ≈ 4.73
δ₂ = Δ₂ / Δ₃ = 0.095 / 0.0247 ≈ 3.85
δ₃ = Δ₃ / Δ₄ → converge a 4.6692
```

**Conclusión:** Cada bifurcación ocurre δ⁻¹ ≈ 21% más cerca que la anterior.

---

## 4. Universalidad de Feigenbaum

### El Teorema

Si un sistema unimodal (con 1 máximo) bifurca período-doble hacia caos, el ratio de espaciamiento tiende a δ ≈ 4.6692 **sin importar el sistema específico**.

### Ejemplos de Universalidad

| Sistema | δ Observado |
|---------|------------|
| Mapa logístico | 4.6692 |
| Mapa tienda | 4.6692 |
| Oscilador forzado | 4.6692 |
| Reacción Belousov-Zhabotinsky | 4.6692 |
| Población: P_{n+1} = r·P(1-P/K) | 4.6692 |
| Circuito electrónico con diodo | 4.6692 |

**¿Por qué?** La bifurcación período-doble depende de la estructura local (derivada f'(x)) no de los detalles globales.

---

## 5. Ventanas Periódicas en Caos

### Fenómeno

Dentro de la región caótica (r > 3.57) existen "islas" donde reaparece periodicidad.

### Ejemplo: Ventana Período-3

- **Ubicación:** r ≈ 3.8284
- **Rango:** r ∈ [3.8284, 3.8495]
- **Significado:** Caos NO es ausencia de orden, es orden entrelazado

### Patrón de Ventanas

```
Región caótica:
├─ Ventana período-3
├─ Ventana período-5
├─ Ventana período-6
└─ Muchas más...

Cada ventana tiene su PROPIA cascada período-doble hacia caos.
δ reaparece en cada ventana (universalidad recursiva).
```

---

## 6. Control de Caos (Stabilization)

### Objetivo

Estabilizar una órbita periódica **inestable** que existe dentro del atractor caótico.

### Método: Feedback Proporcional

Perturbación pequeña: **Δx_n = K(x_n - x_target)**

Nueva dinámica: **x_{n+1} = f(x_n + Δx_n)**

Con K pequeño (K ∈ [0.05, 0.20] típico), la órbita inestable se estabiliza.

### Ejemplo

```
Sin control:
x_n → [caos, valores aleatorios]

Con control (K=-0.1):
x_n → [oscila regularmente cerca período-2 inestable]
```

**Implicación:** Caos NO es incontrolable, es altamente controlable con feedback mínimo.

---

## Diccionario Punto 4

| Término | Definición |
|---------|-----------|
| **Feigenbaum δ** | Ratio universal de espaciamiento bifurcaciones ≈ 4.6692 |
| **Período-doble** | Duplicación P → 2P → 4P → 8P → ... |
| **Mapa logístico** | x_{n+1} = r·x(1-x) |
| **Bifurcación** | Cambio cualitativo al variar parámetro |
| **Onset del caos** | r ≈ 3.5699 donde bifurcaciones densas comienzan |
| **Universalidad** | Propiedad idéntica en sistemas distintos |
| **Ventana periódica** | Isla de periodicidad dentro región caótica |
| **Control de caos** | Estabilizar órbita inestable con feedback |
| **Lyapunov λ** | Tasa divergencia (ver CONCEPTOS_GENERALES.md) |
| **Bifurcación silla-nodo** | λ = 1 (eigenvalor real) |
| **Bifurcación período-doble** | λ = -1 (eigenvalor real negativo) |

---

**Para más detalles sobre bifurcaciones, eigenvalores, y caos en general, ver CONCEPTOS_GENERALES.md**
