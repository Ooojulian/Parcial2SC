# Parcial 2 - Sistemas Complejos

Proyecto completo con 5 puntos: Internet topology, Peano arithmetic, Net interactions, Feigenbaum δ, y Attractors.

## Estructura

```
Parcial2SC/
├── CONCEPTOS_GENERALES.md    ← Términos transversales
├── README.md                 ← Este archivo
├── requirements.txt
├── pytest.ini
│
└── Punto_X/ (1-5)
    ├── README.md             ← Qué es el punto
    ├── CONCEPTOS.md          ← Términos específicos
    ├── SOLUCION.md           ← Respuesta clara
    ├── main.py               ← Ejecutable
    ├── src/                  ← Código fuente
    └── tests/                ← Validación
```

## Instalación y Ejecución

```bash
# Instalar dependencias
pip install -r requirements.txt

# Revisar un punto (ejemplo Punto 1)
cd Punto_1
cat README.md      # Leer qué pide
cat SOLUCION.md    # Ver respuesta
python main.py     # Ejecutar código
pytest tests/ -q   # Validar (28 tests)

# Todos los tests
pytest Punto_*/tests/ -q
# Total: 164 tests ✓
```

## Puntos Completados

| Punto | Tema | Tests | SOLUCION.md | Status |
|-------|------|-------|------------|--------|
| **1** | Internet Topology (Scale-free) | 28 ✓ | ✅ | Completo |
| **2** | Peano Arithmetic (Recursión) | 37 ✓ | ✅ | Completo |
| **3** | Net Interactions (FP puro) | 26 ✓ | ✅ | Completo |
| **4** | Feigenbaum δ (Bifurcaciones) | 37 ✓ | ✅ | Completo |
| **5** | Attractors (ABM) | 36 ✓ | ✅ | Completo |
| | **TOTAL** | **164 ✓** | **5/5** | **100%** |

## Flujo de Revisión Recomendado

Para cada punto:

1. **README.md** - Entiende qué pide el parcial
2. **SOLUCION.md** - Lee la respuesta clara
3. **CONCEPTOS.md** - Aprende los términos específicos
4. **python main.py** - Ve el código en acción
5. **pytest tests/ -q** - Valida que funciona

## Conceptos Generales

Para términos que aparecen en múltiples puntos (eigenvalores, bifurcaciones, atractores, etc.), ver:
```bash
cat CONCEPTOS_GENERALES.md
```

## Preguntas Frecuentes

**¿Dónde está la respuesta del Punto X?**
→ Cada punto tiene `SOLUCION.md` que responde directamente qué pide el parcial.

**¿Qué hacen los tests?**
→ Validan que el código implementa correctamente lo solicitado. 164 tests en total, todos pasando.

**¿Dónde está el código?**
→ Carpeta `src/` en cada Punto_X/. `main.py` es el ejecutable que demuestra funcionalidad.

---

**Parcial completado y listo para evaluar** ✓
