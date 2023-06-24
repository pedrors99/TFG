# Trabajo de Fin de Grado
## Implementación de protocolos de conocimiento cero con fines docentes

> Doble Grado en Ingeniería Informática y Matemáticas
>
> **Alumno:** Pedro Ramos Suárez.
>
> **Tutor:** Rafael Alejandro Rodríguez Gómez.
> Departamento de Teoría de la Señal, Telemática y Comunicaciones.
>
> Universidad de Granada.
>
> Curso 2022/2023.

En los últimos años, debido en parte a los ataques de ciberseguridad, la seguridad ha adquirido una gran importancia, especialmente en cualquier proceso online. Esto dificulta compartir información, ya que compartirla puede requerir revelar información confidencial.

Para solucionarlo, surgen los protocolos de conocimiento cero (ZKP), que pretenden demostrar que algo es verdadero o falso sin revelar ninguna información al respecto.

Implementar algoritmos de ZKP es y será fundamental en el próximo futuro así que se espera un aumento de la necesidad de profesionales en este ámbito. Por este motivo, el presente trabajo tiene como objetivo implementar una herramienta que facilite el aprendizaje de estos algoritmos.

# Estructura de la memoria

* 1. Introducción.
    * 1.1. Motivación.
    * 1.2. Solución Propuesta.
    * 1.3. Estructura de la Memoria.
* 2. Contexto de Zero Knowledge Proofs.
    * 2.1. Aplicaciones.
    * 2.2. Marco histórico.
    * 2.3. Protocolos de conocimiento cero en el contexto docente.
* 3. Marco teórico.
    * 3.1. Clases de protocolos de conocimiento cero.
    * 3.2. Algoritmos basados en ZKP.
    * 3.3. Algoritmos ZKRP.
        * 3.3.1. Descomposición cuadrada (**Square decomposition**).
        * 3.3.2. Basado en firma (**Signature-based**).
        * 3.3.3. Bulletproofs.
    * 3.4. Selección de algoritmo.
* 4. Objetivos y planificación.
    * 4.1. Objetivos.
    * 4.2. Planificación.
* 5. Desarrollo de la propuesta
    * 5.1. Implementación de **Square Decomposition**.
        * 5.1.1. Bibliotecas.
        * 5.1.2. Implementación.
    * 5.2. Interfaz de la herramienta.
    * 5.3. Verificación del funcionamiento del algoritmo.
* 6. Conclusiones y Líneas de Trabajo Futuro.
    * 6.1. Conclusiones.
    * 6.2. Líneas de Trabajo Futuro-
* Bibliografía.
* Anexo A. Manual de usuario para la herramienta docente.
    * Ejecución del servidor.
    * Elementos en común.
    * Inicio.
    * Pruebas.
    * Verificaciones.