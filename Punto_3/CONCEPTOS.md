# Conceptos Clave - Punto 3: Net Interactions

**Referencia rápida de términos específicos de Punto 3. Para conceptos generales (eigenvalores, punto fijo, convergencia, etc.), ver CONCEPTOS_GENERALES.md en la raíz.**

**Para explicación completa de por qué FP responde el problema, ver SOLUCION.md**

---

## Términos Específicos de Punto 3

### Red (Network)
Conjunto de nodos conectados por aristas (relaciones)

### Matriz de Pesos W
```
W[i][j] = fuerza de conexión de nodo j a nodo i
W[0][1] = 0.5  →  Nodo 1 influye POSITIVAMENTE en nodo 0
W[0][2] = -0.3 →  Nodo 2 influye NEGATIVAMENTE en nodo 0
```

### Estado (State)
Vector x de valores actuales: `x = [x₀, x₁, x₂, ...]`

### Función de Activación F(·)
Transforma entrada en salida:
- Identity: σ(z) = z
- ReLU: σ(z) = max(0, z)
- Sigmoid: σ(z) = 1/(1 + e^(-z))
- Tanh: σ(z) = (e^z - e^(-z))/(e^z + e^(-z))

### Punto Fijo x*
Estado que NO CAMBIA: `x* = W @ F(x*)`

### Convergencia
Cuando x_n → x* (se estabiliza)

### Eigenvalor λ
Número donde `W·v = λ·v`
- λ_max < 1: convergencia
- λ_max > 1: divergencia

---

## La Interacción (Net Interaction)

**Fórmula:**
```
x_{n+1} = W @ F(x_n)
```

**En 3 pasos funcionales:**
1. `activate(f, x)` = F(x) (aplica f a cada elemento)
2. `weight(W, F(x))` = W @ F(x) (multiplica por W)
3. `aggregate(W @ F(x))` = Σ(W @ F(x)) (suma, opcional)

**Composición:**
```
net_interaction(W, f, x) = weight(W, activate(f, x))
                         = W @ F(x)
```

---

## Paradigma Funcional

✓ **Pureza**: f(x) siempre devuelve lo mismo
✓ **Inmutabilidad**: nunca se modifican inputs
✓ **Composición**: funciones se componen sin "pegajosidad"
✓ **Orden superior**: funciones reciben funciones (f es parámetro)
✓ **Sin efectos secundarios**: no hay mutaciones globales

---

## Dinámica Temporal

```
x₀ = [1.0, -0.5, 0.8]       (estado inicial)
x₁ = W @ F(x₀)              (después de 1 paso)
x₂ = W @ F(x₁)              (después de 2 pasos)
...
x* = W @ F(x*)              (PUNTO FIJO, converge)
```

---

## Estabilidad

Si λ_max(Jacobiano en x*) < 1, entonces:
- El punto fijo x* es **ESTABLE**
- El sistema converge desde cualquier condición inicial
- La trayectoria: x₀ → x₁ → x₂ → ... → x*

---

**Para ejemplo completo: ver SOLUCION.md**
