#!/usr/bin/env python3
"""
Main execution script for Punto 2: Peano Arithmetic.

Demonstrates arithmetic operations and verifies properties.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.arithmetic import S, pred, add, mul, power, verify_properties

if __name__ == "__main__":
    print("\n" + "="*70)
    print("PUNTO 2: ARITMÉTICA DE PEANO")
    print("="*70 + "\n")

    # Successor function
    print("[1] FUNCIÓN SUCESORA (S)")
    print("-" * 70)
    print("Definición: S(n) = n + 1")
    print("Es la ÚNICA operación primitiva.\n")
    print("Ejemplos:")
    for n in [0, 2, 5, 10]:
        print(f"  S({n}) = {S(n)}")
    print()

    # Predecessor function
    print("[2] FUNCIÓN PREDECESOR (pred)")
    print("-" * 70)
    print("Definición: pred(S(n)) = n, pred(0) = 0\n")
    print("Ejemplos:")
    for n in [0, 1, 5, 10]:
        print(f"  pred({n}) = {pred(n)}")
    print()

    # Addition
    print("[3] ADICIÓN (add)")
    print("-" * 70)
    print("Definición recursiva:")
    print("  add(m, 0) = m")
    print("  add(m, S(n)) = S(add(m, n))\n")
    print("Complejidad: Θ(n) tiempo, Θ(n) espacio\n")
    print("Ejemplos:")
    for m, n in [(0, 0), (2, 3), (5, 7), (10, 10)]:
        result = add(m, n)
        print(f"  add({m:2d}, {n:2d}) = {result:2d}")
    print()

    # Multiplication
    print("[4] MULTIPLICACIÓN (mul)")
    print("-" * 70)
    print("Definición recursiva (usando add):")
    print("  mul(m, 0) = 0")
    print("  mul(m, S(n)) = add(mul(m, n), m)\n")
    print("Complejidad: Θ(m·n) tiempo, Θ(n) espacio\n")
    print("Ejemplos:")
    for m, n in [(0, 5), (1, 7), (2, 3), (4, 5)]:
        result = mul(m, n)
        print(f"  mul({m:2d}, {n:2d}) = {result:2d}")
    print()

    # Power
    print("[5] POTENCIA (power)")
    print("-" * 70)
    print("Definición recursiva (usando mul):")
    print("  power(m, 0) = 1")
    print("  power(m, S(n)) = mul(power(m, n), m)\n")
    print("Complejidad: Θ(m^n) tiempo, Θ(n) espacio\n")
    print("Ejemplos:")
    for m, n in [(2, 0), (2, 1), (2, 3), (3, 3)]:
        result = power(m, n)
        print(f"  power({m:2d}, {n:2d}) = {result:2d}")
    print()

    # Properties
    print("[6] PROPIEDADES ALGEBRAICAS")
    print("-" * 70)
    props = verify_properties(max_n=10)

    print("Verificadas para n ∈ [0, 9]:\n")
    print(f"  Conmutatividad suma:      {props.commutativity_add}")
    print(f"  Asociatividad suma:       {props.associativity_add}")
    print(f"  Identidad suma (0):       {props.identity_add}")
    print(f"  Conmutatividad mult:      {props.commutativity_mul}")
    print(f"  Asociatividad mult:       {props.associativity_mul}")
    print(f"  Identidad mult (1):       {props.identity_mul_left and props.identity_mul_right}")
    print(f"  Distributividad:          {props.distributivity}")
    print(f"  Principio de inducción:   {props.induction_holds}")
    print()

    # Summary
    all_ok = (
        props.commutativity_add and props.associativity_add and
        props.identity_add and props.commutativity_mul and
        props.associativity_mul and props.identity_mul_left and
        props.identity_mul_right and props.distributivity and
        props.induction_holds
    )

    if all_ok:
        print("✓ TODAS LAS PROPIEDADES VERIFICADAS")
    else:
        print("✗ ALGUNAS PROPIEDADES FALLARON")

    print("="*70 + "\n")
