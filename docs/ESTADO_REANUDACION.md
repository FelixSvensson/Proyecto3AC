> Registro histórico. Para el estado vigente, consultar [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md).

# Estado guardado para reinicio - 28 de octubre de 2026

El usuario pidió guardar todo para reiniciar Windows ahora. No reiniciar automáticamente.

## Trabajo realizado

- Clon independiente de https://github.com/FelixSvensson/Proyecto2AC con historial completo en este directorio Proyecto3AC.
- Rama local main, revisión fuente 67d0c48bcc115614a4029ff024277cb53bc30a05, del 21 de octubre de 2026.
- Se inspeccionaron main y proyecto2/dev-game. Esta última apunta a 6c0f7c69c656bc7226278f66ab4bd390bc12e820, del 13 de octubre; main es posterior e incluye Informe_Proyecto2.pdf. Se prioriza main.
- El remoto de origen se llama proyecto2. Se añadió origin apuntando a https://github.com/FelixSvensson/Proyecto3AC.git. Esto NO crea el repositorio remoto; su existencia y permisos están pendientes.
- No se modificó el repositorio original, no se crearon commits y no se ejecutó push. Los archivos RTL clonados siguen intactos.
- Se guardaron los requisitos completos en docs/REQUISITOS_PROYECTO.md.
- Se instaló Microsoft WSL 2.7.14.0 mediante winget elevado. Kernel informado: 6.18.33.2-2. Log real: results/environment/wsl-install-admin.log.
- Se ejecutó la instalación de Ubuntu-24.04 con --no-launch. Windows habilitó componentes y respondió que requieren reinicio. NO hay distribución Ubuntu registrada todavía.
- Equipo: Windows build 26200.9711 (DisplayVersion 25H2; la etiqueta heredada de ProductName devuelve Windows 10 Pro), 14 procesadores lógicos, 33.745.166.336 bytes de RAM, aproximadamente 405 GB libres inicialmente.
- Git no devolvió user.name ni user.email efectivos. No se configuraron identidades ni correos.

## Hallazgos técnicos iniciales

- rtl/pochoco_soc.v usa por_cnt inicializado para generar reset de encendido.
- rtl/pochoco_ram.v usa initial y $readmemh, con lecturas síncronas. Debe preservarse su latencia.
- rtl/espino_core/espino_register_file.v instancia primitivas iCE40 SB_RAM40_4K y duplica el banco para dos puertos de lectura. Es una dependencia tecnológica adicional que debe migrarse a FF manteniendo lectura síncrona y x0.
- rtl/pochoco_periph.v contiene cycle_q y led_cycle_q de 32 bits.
- sw/game.s en main carga para la espera lui x6,0xEE6b y addi x6,x6,640: debe calcularse el valor real y documentar la discrepancia con el informe, sin asumir 75.000.000.
- El informe original identifica al Grupo 15: Martin Heiremans, Felix Svensson y Juan Pablo Saavedra. Profesor: Jorge Gómez Mir. El informe declara 107 instrucciones y ausencia de pila/RAM de datos; todavía falta verificarlo mediante ensamblado y ejecución real.
- No se ejecutaron tests, simulaciones, síntesis, PnR ni signoff. No hay métricas de área/timing, GDSII ni PDFs nuevos. No declarar entrega terminada.

## Reanudar después del reinicio

1. Comprobar `wsl --status` y `wsl --list --verbose`.
2. Si no hay distribución, ejecutar `wsl --install -d Ubuntu-24.04 --no-launch` y comprobar el resultado real. Puede requerir elevación. No borrar ni reinstalar distribuciones existentes.
3. Inicializar Ubuntu y verificar ejecución mediante `wsl -d Ubuntu-24.04 -- uname -a`. Si pide usuario/contraseña, dejar que el usuario elija sus credenciales; no inventarlas.
4. Continuar con instalación soportada de LibreLane. Se consultó documentación oficial: https://librelane.readthedocs.io/en/stable/installation/appimage_installation/installation_win.html y https://librelane.readthedocs.io/en/stable/usage/about_pdks.html. Esta última recomienda GF180MCU D y revisión compatible descargada con Ciel. Fijar versiones reales y probar el entorno antes de corridas costosas.
5. Retomar todas las fases y criterios del documento REQUISITOS_PROYECTO.md. No limitar el trabajo a la instalación de Ubuntu.

## Recursos adicionales

- Python disponible: C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe.
- En work/ (fuera de este repositorio) se descargó OSS CAD Suite Windows 2025-02-13 como alternativa para pruebas nativas. No se ejecutó ni extrajo. SHA256: FA7F8F827C7FCBC9BB9F2FEE5FC41ECB5F57F659CED661EE4E4BBAF9E520AD36. Preferir una instalación Linux compatible y homogénea para el flujo final; no mezclar métricas entre versiones.
- El PDF oficial Proyecto_3_arquitectura.pdf no apareció en la búsqueda de PDFs dentro de attachments. El enunciado transcrito permite continuar.

## Política invariable

Nunca ejecutar git commit, git push, commits por API, merges con commit, reescritura de historia ni reset --hard. Preparar cambios sin publicar y al finalizar entregar los comandos para que el usuario haga personalmente el commit y push con su identidad real.
