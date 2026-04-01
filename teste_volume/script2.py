import sys
print("Argumentos de linha de comando:", sys.argv)
arg1 = sys.argv[1] if len(sys.argv) > 1 else "Valor padrão para arg1"
arg2 = sys.argv[2] if len(sys.argv) > 2 else "Valor padrão para arg2"
print(f"Argumento 1: {arg1}")
print(f"Argumento 2: {arg2}")
