# Verifiers

Este módulo maneja toda la lógica de validación.

## Responsabilidades
- Asegurar la consistencia y corrección de los datos antes de que lleguen a la base de datos.
- Validar disponibilidad de stock, existencia de entidades y cantidades negativas.
- Manejar tanto validaciones basadas en DataFrame como validaciones de entradas individuales.

## Implemented verifications
There's two kinds of verifications:
1. Products verifications:
    - All positive values 
    - All products names inserted in the dataframe match with the database records
2. Raw material verifications:
    - All positive values
    - All raw material names inserted in the dataframe match with the database records
    - In case of `stock-out`, checks if the entered amount surpasses the stored amount 