# Conceptos Clave - Punto 1: Internet Topology

**Para conceptos generales (grafos, distribuciones, redes escala-libre, clustering, etc.), ver CONCEPTOS_GENERALES.md en la raíz.**

---

## 1. Modelo de Internet

### Internet como Grafo

```
G = (V, E, W)

V = nodos (routers, servidores, ASNs)
E = aristas (enlaces físicos/lógicos)
W = pesos (ancho de banda, latencia, costo BGP)
```

### Grado (Degree)

Número de conexiones de un nodo.

**Tipos:**
- **In-degree:** Aristas entrantes
- **Out-degree:** Aristas salientes
- **Grado total:** in + out

**En Internet:** Hubs Tier-1 tienen grado ~100+

---

## 2. Propiedades de Internet

### Distribución de Grados

**Internet:** Sigue **ley de potencia** P(k) ∼ k^{-γ}

- γ ≈ 2.1-2.5 (escala-libre)
- Hubs gigantes coexisten con nodos periféricos
- Emergente de **apego preferencial**: nodos nuevos se conectan con probabilidad proporcional al grado actual

### Pequeño Mundo (Small World)

- **Distancia promedio:** d ≈ 3.7 saltos (nivel ASN)
- **Diámetro:** ~15-20 saltos (máximo)
- **Implicación:** Cualquier router está a pocos saltos de otro

### Clustering

**Coeficiente:** C ≈ 0.01-0.03 (bajo pero > red aleatoria)

**Significado:** Si A y C comparten cliente B, probablemente A y C también tienen relación directa

---

## 3. Modelo Barabási-Albert (BA)

### Mecanismo: Apego Preferencial

Nodo nuevo se conecta a nodo i con probabilidad:

$$P(\text{conectar a } i) = \frac{k_i}{\sum_j k_j}$$

**"Los ricos se hacen más ricos"**

### Resultado

Genera automáticamente distribución ley de potencia P(k) ∼ k^{-3}

---

## 4. Robustez y Vulnerabilidad

### Percolación (Molloy-Reed Theorem)

Red colapsa su componente gigante cuando fracción f de nodos se elimina:

$$f_c = 1 - \frac{1}{\kappa - 1}, \quad \kappa = \frac{\langle k^2 \rangle}{\langle k \rangle}$$

### Implicación para Internet

- **Fallos aleatorios:** f_c ≈ 0.95 (tolera 95% de fallos aleatorios)
- **Ataques dirigidos:** Muy frágil (vulnerabilidad a DDoS en hubs)
- Diferencia asimétrica entre robustez y fragilidad

---

## 5. Enrutamiento

### BGP (Border Gateway Protocol)

Protocolo distribuido que computa rutas entre ASNs.

**Características:**
- Descentralizado (cada nodo decide autonomamente)
- Convergencia: O(n²) en peor caso
- Puede oscilar (oscilaciones BGP, ciclos inestables)

### Shortest Path Routing

Problema fundamental: encontrar camino más corto.

**NP-difícil globalmente, pero BGP lo aproxima bien en escala-libre** (O(diameter) ≈ 4 pasos típico)

---

## 6. Diccionario Punto 1

| Término | Definición |
|---------|-----------|
| **Escala-libre** | P(k) ∼ k^{-γ}, no hay escala característica |
| **Apego preferencial** | Nodos nuevos se conectan proporcional a grado actual |
| **Hubs** | Nodos con grado muy alto (centrales) |
| **Pequeño mundo** | Distancia promedio O(log N) |
| **Clustering** | "Amigos de amigos son amigos" |
| **Grado** | Número de conexiones de un nodo |
| **Distribución Poisson** | Red aleatoria (mayoría de nodos grado medio) |
| **Ley de potencia** | Red escala-libre (hubs gigantes) |
| **Percolación** | Colapso de conectividad por fallos/ataques |
| **BGP** | Protocolo de enrutamiento distribuido |
| **Convergencia** | Proceso de encontrar rutas estables |
| **Robustez** | Tolerancia a fallos aleatorios |
| **Fragilidad** | Vulnerabilidad a ataques dirigidos |

---

**Para más detalles sobre redes, distribuciones, y topología en general, ver CONCEPTOS_GENERALES.md**
