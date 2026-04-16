# Conceptos Clave - Punto 2: Peano Arithmetic

**Para conceptos generales (recursión, inducción, función pura, etc.), ver CONCEPTOS_GENERALES.md en la raíz.**

---

## 1. Los 5 Axiomas de Peano

### PA1: Cero es Natural
```
0 ∈ ℕ
```
"Existe un número base llamado cero"

### PA2: Sucesor
```
∀n ∈ ℕ: S(n) ∈ ℕ
```
"Para todo número, existe un siguiente número"

Ejemplos: S(0)=1, S(5)=6

### PA3: Cero No es Sucesor
```
∀n ∈ ℕ: S(n) ≠ 0
```
"Ningún número tiene cero como sucesor"

### PA4: Inyectividad
```
∀m,n ∈ ℕ: S(m) = S(n) ⟹ m = n
```
"Diferentes números tienen diferentes sucesores"

### PA5: Inducción
```
Si cierto en 0 y en todo sucesor, cierto en todos
```

---

## 2. Construcción de Números Naturales

Cada número es secuencia de aplicaciones de S desde 0:

```
0       = 0
1       = S(0)
2       = S(S(0))
3       = S(S(S(0)))
n       = S aplicado n veces desde 0
```

---

## 3. Suma Recursiva

### Definición (add)

```
add(m, 0) = m                         [caso base]
add(m, S(n)) = S(add(m, n))          [paso recursivo]
```

### Interpretación

Sumar n es aplicar S a m exactamente n veces.

### Ejemplo: add(2, 3)

```
add(2, 3) = add(2, S(2))
          = S(add(2, 2))
          = S(add(2, S(1)))
          = S(S(add(2, 1)))
          = S(S(add(2, S(0))))
          = S(S(S(add(2, 0))))
          = S(S(S(2)))
          = 5
```

**Conclusión:** add(2,3) aplicó S tres veces a 2 → 2→3→4→5

---

## 4. Multiplicación Recursiva

### Definición (mul)

```
mul(m, 0) = 0                        [caso base]
mul(m, S(n)) = add(mul(m, n), m)    [paso recursivo]
```

### Interpretación

Multiplicar m por n es sumar m exactamente n veces.

### Ejemplo: mul(2, 3)

```
mul(2, 3) = add(mul(2, 2), 2)
          = add(add(mul(2, 1), 2), 2)
          = add(add(add(mul(2, 0), 2), 2), 2)
          = add(add(add(0, 2), 2), 2)
          = add(add(2, 2), 2)
          = add(4, 2)
          = 6
```

**Conclusión:** mul(2,3) sumó 2 tres veces → 0→2→4→6

---

## 5. Propiedades Aritméticas Probadas

### Commutativity (Conmutatividad)

**add(m, n) = add(n, m)**

Prueba: Por inducción sobre n

**mul(m, n) = mul(n, m)**

Prueba: Por inducción sobre n

### Associativity (Asociatividad)

**add(add(m, n), p) = add(m, add(n, p))**

Prueba: Por inducción sobre p

**mul(mul(m, n), p) = mul(m, mul(n, p))**

Prueba: Por inducción sobre p

### Distributivity (Distributividad)

**mul(m, add(n, p)) = add(mul(m, n), mul(m, p))**

Prueba: Por inducción sobre p

---

## 6. Potencia

### Definición (pow)

```
pow(m, 0) = 1                          [caso base]
pow(m, S(n)) = mul(pow(m, n), m)     [paso recursivo]
```

**Equivalente:** m^n es multiplicar m por sí mismo n veces

---

## 7. Predecesor

### Definición (pred)

```
pred(0) = 0                    [caso especial]
pred(S(n)) = n                [inversa de sucesor]
```

**Propiedad:** pred es el inverso de S (excepto en 0)

---

## 8. Complejidad de Operaciones

| Operación | Complejidad | Razón |
|-----------|------------|-------|
| add(m, n) | Θ(n) | n aplicaciones de S |
| mul(m, n) | Θ(m·n) | n llamadas a add |
| pow(m, n) | Θ(m^n) | n llamadas a mul |

**Conclusión:** Aritmética Peano es correcta pero ineficiente (O(n) para suma vs O(1) binaria)

---

## 9. Diccionario Punto 2

| Término | Definición |
|---------|-----------|
| **Axioma** | Verdad asumida sin demostración |
| **Peano axioms** | 5 axiomas que definen naturales desde S y 0 |
| **Sucesor S(n)** | Siguiente número después de n |
| **Recursión** | Definir en términos de versiones más simples |
| **Inducción** | Prueba encadenada: base + paso → conclusión |
| **add(m,n)** | Suma recursiva vía S |
| **mul(m,n)** | Multiplicación recursiva vía add |
| **pow(m,n)** | Potencia recursiva vía mul |
| **pred(n)** | Predecesor (inverso de S) |
| **Conmutatividad** | add(m,n) = add(n,m) |
| **Asociatividad** | add(add(m,n),p) = add(m,add(n,p)) |
| **Distributividad** | mul(m, add(n,p)) = add(mul(m,n), mul(m,p)) |

---

**Para más detalles sobre recursión, inducción, y funciones puras en general, ver CONCEPTOS_GENERALES.md**
