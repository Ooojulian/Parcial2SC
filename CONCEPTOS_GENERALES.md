# Conceptos Generales - Sistemas Complejos

Términos y conceptos que aparecen en **múltiples puntos** del parcial.

---

## 1. Sistemas Dinámicos y Atractores

### Punto Fijo (Fixed Point)
Estado donde x* = f(x*). El sistema no cambia.

**Ejemplos:**
- Punto 3: x* = W @ F(x*) en red de interacciones
- Punto 5: Equilibrio en sistema de Lorenz cuando ρ < 1

### Órbita Periódica (Periodic Orbit)
Estado que repite cada T pasos: x_{n+T} = x_n

**Ejemplos:**
- Punto 4: Período-2, período-4, período-8 en cascada hacia caos
- Punto 5: Ciclo límite (período T en oscilador)

### Atractor
Conjunto invariante que atrae órbitas cercanas.

| Tipo | Dimensión | Propiedades |
|------|-----------|------------|
| Punto fijo | 0 | Equilibrio, convergencia exponencial |
| Ciclo límite | 1 | Oscilación periódica aislada |
| Toro | 2+ | Quasiperiodicidad |
| Atractor extraño | Fraccionaria | Caos, estructura fractal |

---

## 2. Bifurcaciones

### Bifurcación (Bifurcation)
Cambio cualitativo en comportamiento dinámico cuando varías parámetro.

**Tipos principales:**

| Tipo | Descripción | Parámetro Crítico |
|------|-------------|-------------------|
| **Silla-nodo** | Punto fijo desaparece | λ = 1 |
| **Período-doble** | Órbita período-T → período-2T | λ = -1 |
| **Hopf** | Punto fijo → ciclo límite | Eigenvalor cruza ℑ(λ) = 0 |
| **Pitchfork** | Bifurcación asimétrica (3 ramas) | Simetría rota |

**Ejemplos en parcial:**
- Punto 3: Estabilidad determinada por λ_max
- Punto 4: Período-doble en cascada (r = 3, 3.449, 3.544, ...)
- Punto 5: Hopf bifurcation en Lorenz (ρ = 24.74)

---

## 3. Estabilidad y Eigenvalores

### Eigenvalor (Eigenvalue)
Número λ donde J·v = λ·v (J = Jacobiano, v = eigenvector)

### Jacobiano (Jacobian Matrix)
Matriz de derivadas parciales de f en punto x*:

$$J_{ij} = \frac{\partial f_i}{\partial x_j}\Big|_{x*}$$

### Criterio de Estabilidad
Para punto fijo x*:
- **|λ_max| < 1**: Atractor (convergencia)
- **|λ_max| = 1**: Bifurcación
- **|λ_max| > 1**: Repulsor (divergencia)

**Ejemplos:**
- Punto 3: λ_max = 0.2023 < 1 → ESTABLE
- Punto 4: λ_max cruza -1 en r=3 → bifurcación período-doble
- Punto 5: Lorenz tiene 3 eigenvalores reales (determina tipo atractor)

---

## 4. Caos y Lyapunov

### Lyapunov Exponent (λ_Lyapunov)
Tasa promedio de divergencia exponencial de órbitas cercanas:

$$\lambda = \lim_{n \to \infty} \frac{1}{n} \sum_{i=0}^{n-1} \ln |f'(x_i)|$$

### Interpretación
| λ | Comportamiento | Predictibilidad |
|---|----------------|-----------------|
| λ < -0.5 | Convergencia rápida | Muy predecible |
| -0.5 < λ < 0 | Convergencia lenta | Predecible |
| λ ≈ 0 | Transición (bifurcación) | Marginal |
| 0 < λ < 0.5 | Caos débil | Impredecible (~10 pasos) |
| λ > 0.5 | Caos fuerte | Muy impredecible (~2 pasos) |

**Ejemplos:**
- Punto 2 (Peano): Convergencia lineal (λ < 0)
- Punto 3: λ_max < 1 indica convergencia a punto fijo
- Punto 4: λ > 0 en región caótica (r > 3.57)
- Punto 5: Lorenz con ρ=28 tiene λ ≈ 0.9 (caos moderado)

---

## 5. Universalidad

### Universalidad (Universality)
Propiedad que aparece **independientemente** de los detalles específicos del sistema.

**Ejemplo clave:** Constante de Feigenbaum δ ≈ 4.6692 aparece en:
- Mapas logísticos
- Circuitos electrónicos
- Reacciones químicas
- Poblaciones biológicas
- Cualquier mapa unimodal

### Renormalización
Técnica que explica por qué sistemas diferentes convergen a universalidad.

Idea: Si escalas variables y parámetros correctamente, ecuaciones diferentes se ven iguales localmente.

---

## 6. Dinámicas Acopladas

### Sistema Acoplado
Múltiples variables que se influyen mutuamente: **x_{n+1} = f(x_n, y_n); y_{n+1} = g(x_n, y_n)**

**Ejemplos:**
- Punto 3: Red de N nodos donde cada uno influye en todos: x_{n+1} = W @ F(x_n)
- Punto 5: Lorenz con 3 variables acopladas (x, y, z)

### Matriz de Acoplamiento (Coupling Matrix)
Define la topología de influencias:

$$W_{ij} = \text{fuerza de acoplamiento de j→i}$$

**En Punto 3:** W es la matriz de pesos de la red

**En Punto 5:** W es implícita en ecuaciones diferenciales

---

## 7. Redes Complejas

### Red Scale-Free (Scale-Free Network)
Distribución de grados sigue ley de potencia: **P(k) ∼ k^{-γ}**

**Propiedades:**
- Hubs gigantes coexisten con nodos periféricos
- Robusta a fallos aleatorios pero frágil a ataques dirigidos
- Emergen de apego preferencial

**Ejemplo:** Punto 1 - Internet tiene γ ≈ 2.1-2.5

### Apego Preferencial (Preferential Attachment)
Nodo nuevo se conecta con probabilidad proporcional al grado actual:

$$P(\text{conectar a } i) = \frac{k_i}{\sum_j k_j}$$

"Los ricos se hacen más ricos"

---

## 8. Aritmética Recursiva

### Recursión (Recursion)
Función definida en términos de sí misma + caso base

**Ejemplo - Punto 2:**
```
add(m, 0) = m                      [base]
add(m, S(n)) = S(add(m, n))       [recursivo]
```

### Inducción Matemática
Método de prueba:
1. Base: Probar para n=0
2. Paso: Asumir cierto para n, probar para S(n)
3. Conclusión: Verdadero para todo ℕ

**Punto 2 lo aplica para probar:** add(m,n) = m+n, mul(m,n) = m·n, etc.

---

## 9. Integración Numérica

### Runge-Kutta (RK4)
Método para resolver ODEs (ecuaciones diferenciales ordinarias):

$$\frac{dx}{dt} = f(x, t)$$

**Algoritmo básico:**
```
k1 = f(x_n, t_n)
k2 = f(x_n + dt·k1/2, t_n + dt/2)
k3 = f(x_n + dt·k2/2, t_n + dt/2)
k4 = f(x_n + dt·k3, t_n + dt)
x_{n+1} = x_n + (dt/6)·(k1 + 2k2 + 2k3 + k4)
```

**Ventaja:** Error O(dt^5), muy preciso

**Ejemplo:** Punto 5 integra Lorenz con RK4

---

## 10. Programación Funcional

### Función Pura (Pure Function)
Función sin efectos secundarios:
- Output depende solo del input
- No modifica estado global
- f(x) siempre devuelve lo mismo

**Ejemplo - Punto 3:**
```python
def activate(f, state):
    return np.array([f(x) for x in state])  # pura
```

### Composición de Funciones (Function Composition)
Combinar funciones: (f ∘ g)(x) = f(g(x))

**Ejemplo - Punto 3:**
```
net_interaction = weight ∘ activate
x_new = weight(activate(f, x))
```

### Map y Reduce
- **Map**: Aplicar función a cada elemento
- **Reduce**: Combinar elementos en resultado

**Ejemplo - Punto 3:**
- `activate()` es **map** de f sobre state
- `weight()` es **reduce** vía matriz

---

## 11. Convergencia y Tolerancia

### Convergencia
Sistema se estabiliza cuando cambios son menores que tolerancia:

$$\max|x_{n+1} - x_n| < \epsilon$$

Común usar ε = 10^{-6} o 10^{-8}

**Ejemplos:**
- Punto 2: Peano arithmetic converge en O(n) pasos
- Punto 3: Red converge a punto fijo
- Punto 5: Lorenz es caótico pero órbitas quedan en atractor

---

## 12. Diccionario Técnico Cruzado

| Término | Símbolo | Concepto | Puntos |
|---------|---------|---------|--------|
| Eigenvalor | λ | Número especial de matriz | 3, 4, 5 |
| Jacobiano | J | Matriz de derivadas | 3, 4, 5 |
| Lyapunov exponent | λ_L | Divergencia exponencial | 4, 5 |
| Atractor | A | Conjunto invariante | 3, 4, 5 |
| Bifurcación | - | Cambio cualitativo | 4, 5 |
| Punto fijo | x* | f(x*) = x* | 2, 3, 5 |
| Órbita periódica | - | Período T | 4, 5 |
| Caos | - | λ > 0, sensible CI | 4, 5 |
| Red escala-libre | G | P(k) ∼ k^{-γ} | 1 |
| Función pura | f | Sin efectos laterales | 2, 3 |
| Convergencia | ε | |x_{n+1} - x_n| < ε | 2, 3, 5 |
| Universalidad | δ | Propiedad invariante | 4 |

---

