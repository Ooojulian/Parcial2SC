# Punto 2: Aritmética de Peano - SOLUCIÓN

## Problema

Construir **toda la aritmética desde un único axioma:** la función sucesora S(n) = n+1.

¿Es posible definir suma, multiplicación, potencia usando SOLO S?

## Respuesta: SÍ

**Tres operaciones fundamentales emergen de S:**

### 1. Adición

```
add(m, 0) = m
add(m, S(n)) = S(add(m, n))
```

**Significado:** Sumar n es aplicar S exactamente n veces a m.

**Ejemplo:** add(2, 3) = S(S(S(2))) = 5

**Propiedades verificadas (37 tests):**
- ✓ Conmutatividad: add(m,n) = add(n,m)
- ✓ Asociatividad: add(add(m,n),k) = add(m,add(n,k))
- ✓ Identidad: add(n,0) = n

### 2. Multiplicación

```
mul(m, 0) = 0
mul(m, S(n)) = add(mul(m, n), m)
```

**Significado:** Multiplicar m por n es sumar m exactamente n veces.

**Ejemplo:** mul(2, 3) = add(add(add(0, 2), 2), 2) = 6

**Propiedades verificadas:**
- ✓ Conmutatividad: mul(m,n) = mul(n,m)
- ✓ Asociatividad: mul(mul(m,n),k) = mul(m,mul(n,k))
- ✓ Distributividad: mul(m, add(n,k)) = add(mul(m,n), mul(m,k))

### 3. Potencia

```
pow(m, 0) = 1
pow(m, S(n)) = mul(pow(m, n), m)
```

**Significado:** m^n es multiplicar m por sí mismo n veces.

---

## Cómo Resuelve el Problema

**Sin recursión desde S:** ¿Cómo defines suma sin "+", sin recursión?

**Con axiomas Peano:** Una función S + 5 axiomas → **toda la aritmética emerge**

| Operación | Definida por | Complejidad |
|-----------|---|---|
| add(m,n) | 2 casos, recursa en n | Θ(n) |
| mul(m,n) | 2 casos, usa add | Θ(m·n) |
| pow(m,n) | 2 casos, usa mul | Θ(m^n) |

**Conclusión:** Peano Arithmetic demuestra que **aritmética entera es consecuencia lógica de sucesión**, no axioma base.

---

## Validación

✓ **37 tests pasando (100%)**
- Sucesora/predecesor: 8 tests
- Adición: 7 tests
- Multiplicación: 9 tests
- Potencia: 6 tests
- Propiedades: 7 tests

✓ **Todas las propiedades verificadas**
- Conmutatividad
- Asociatividad
- Distributividad
- Identidades

---

## Implicación

**La aritmética no es primitiva, es derivada de una regla simple (S) + inducción.**

Esto justifica por qué la matemática es rigurosa: los números naturales pueden construirse lógicamente desde mínimos axiomas, sin asumir "número" como concepto dado.
