# Se pueden parsear bits con and y or, de ahi se pueden ir haciendo shifts
# Por ejemplo, 111 & 101 -> 101 (Verifica si hay bits prendidos)
#              000 | 010 -> 010 (Se usa para prender y apagar)
# Para el resolver, yo voy a tener por ejemplo 001001010010
# pero solo meinteresan por ejemplo el tercero y el cuarto, y ahi hago
# blablabla & 001100000000

# Pero nosotros lo vamos a hacer con hexadecimas -> 88 & 18 => 8
# Por dentro, se entiende que lo pasa a bits y lo hace asi

# Parsing se puede hacer con libreria

