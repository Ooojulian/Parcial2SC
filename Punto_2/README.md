# Punto 2: Peano Arithmetic - Operaciones desde Función Sucesora

## ¿Qué es el Punto?

Implementar **suma y multiplicación** usando **solo** la función sucesora S(n) = n+1.

Muestra que toda la aritmética emerge de un axioma simple: aplicar S desde 0 define todos los números naturales.

Números: 0, S(0)=1, S(S(0))=2, S(S(S(0)))=3, ...

## Objetivos

Demostrar propiedades aritméticas formales:
1. ✓ Construcción recursiva (add, mul, power desde S)
2. ✓ Commutativity: add(m,n) = add(n,m)
3. ✓ Associativity: add(add(m,n),p) = add(m,add(n,p))
4. ✓ Distributivity: mul(m, add(n,p)) = add(mul(m,n), mul(m,p))
5. ✓ Induction proof of correctness

## Cómo Ejecutar

**Ver la respuesta (análisis de propiedades):**
```bash
python main.py
```

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
cat src/arithmetic.py
```

**Validar (37 tests):**
```bash
pytest tests/ -q
```
