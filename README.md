# Proyecto 3: Pochoco SoC de FPGA a ASIC

Universidad de los Andes, Arquitectura de Computadores, 2026-2. Grupo 15:
Martin Heiremans, Felix Svensson y Juan Pablo Saavedra. Profesor: Jorge Gómez Mir.

Las métricas canónicas de las corridas terminadas están en `results/summary.csv`
y `results/runs/*/corners.csv`.

## Procedencia

Clon independiente de [Proyecto2AC](https://github.com/FelixSvensson/Proyecto2AC),
main, revisión `67d0c48bcc115614a4029ff024277cb53bc30a05`, con historial completo.
Se inspeccionó dev-game y se priorizó main por ser posterior y contener el
informe entregado.

## Arquitectura y carpetas

Espino utiliza datos de 32 bits, 16 registros RV32E y x0 constante. Conserva el
subconjunto del Proyecto 2, sin desplazamientos ni extensión M. `asic_top`
expone clock, reset explícito activo bajo, cuatro botones, cuatro LED, dos
displays y SPI. Son terminales lógicos de un macro, sin pads ni encapsulado.

El banco iCE40 se reemplaza por FF con dos lecturas síncronas y lectura anterior
a escritura. Se conserva el protocolo del controlador. El contador se separa
para medir área y trazar instancias. Mantener reset activo varios flancos y
desactivarlo cumpliendo timing; el integrador debe respetar las restricciones
de los puertos. El macro no incorpora pads ni debounce.

- `rtl/`: fuentes FPGA conservadas; `asic/rtl/`: reemplazos ASIC.
- `asic/variants/`: optimización de memoria; `asic/configs/`: experimentos.
- `asic/constraints/`: orden funcional de terminales.
- `sw/game.s`: producción a 10 MHz; `sw/game_fpga_original.s`: fuente entregado.
- `asic/generated/`: ROM/programa de producción; `sim/generated/`: abreviado.
- `scripts/`, `results/`, `docs/`: automatización, evidencia y documentos.
- El Makefile original se conserva; los comandos ASIC usan `Makefile.asic`.

## Instalación ejecutada y versiones

Windows build 26200; WSL 2.7.14.0; Ubuntu 24.04.5 LTS. En Windows:

```powershell
wsl --install -d Ubuntu-24.04
wsl --list --verbose
```

Reiniciar si Windows lo pide. En Ubuntu, instalar curl, uidmap, locales,
libfuse2t64, iverilog, python3-venv, make, git, fonts-liberation2 y poppler-utils mediante apt.
Generar la locale en_US.UTF-8. LibreLane se instaló mediante la AppImage oficial:

```bash
sudo mkdir -p /opt/proyecto3-tools
sudo curl -fL --retry 3 https://github.com/librelane/librelane/releases/download/3.0.17/librelane-devshell-x86_64.AppImage -o /opt/proyecto3-tools/librelane-3.0.17.AppImage
sudo chmod +x /opt/proyecto3-tools/librelane-3.0.17.AppImage
sha256sum /opt/proyecto3-tools/librelane-3.0.17.AppImage
```

SHA256 real: `c8ef5ae26b1fc53dd1dd30fe2f1a1da6ab0fdf471dd5a94c2b85d2b3db36833c`.
La instalación de WSL se ejecutó como root. Para otro usuario, el directorio de
PDK debe permitir escritura a Ciel.

Herramientas del entorno coherente: LibreLane 3.0.17, Yosys 0.62, KLayout 0.30.7,
Magic 8.3.623, Netgen 1.5.316, OpenROAD
`dcf36133a369abc8f3c5e5738cd4d82e4903c0e0`, OpenSTA
`857316ff001b2a8dbbdc5996944d08a6d38c87ab`. Ver revisiones y parches en
`results/environment/librelane_tool_versions.txt`. La síntesis mapeada utiliza
siempre el Yosys de la AppImage, no el paquete opcional de Ubuntu.

### GF180MCU

Ciel instala la revisión compatible de Open PDKs
`54435919abffb937387ec956209f9cf5fd2dfbee`, variante **gf180mcuD**, biblioteca
**gf180mcu_fd_sc_mcu7t5v0**, fuera del repositorio en
`/opt/proyecto3-tools/pdks/ciel/gf180mcu/versions/<revision>/gf180mcuD`.

```bash
/opt/proyecto3-tools/librelane-3.0.17.AppImage librelane --pdk gf180mcuD --pdk-root /opt/proyecto3-tools/pdks --smoke-test
```

La prueba pasó; log en results/environment/librelane-smoke.log. Pasar --pdk
explícitamente. Documentación: [LibreLane](https://librelane.readthedocs.io/en/stable/),
[GF180MCU](https://gf180mcu-pdk.readthedocs.io/en/latest/),
[OpenROAD](https://openroad.readthedocs.io/en/latest/).

## Programa, assembler y memorias

```bash
make -f Makefile.asic generate
python3 assembler/assembler.py sw/game.s sw/game.hex
python3 assembler/assembler.py sw/game.s sw/game.hex --rom-dir asic/generated
make -f Makefile.asic verify
```

Hay 107 instrucciones (428 bytes). El juego usa cero palabras de RAM: todos
los accesos son MMIO y el estado vive en registros. Se reserva una palabra en
0x1AC para datos y pruebas. A (`MemoryStrategy=0`) usa ROM combinacional y RAM
mínima; B (`MemoryStrategy=1`) contiene 108 palabras FF, incluidas instrucciones
reescribibles, restauradas mediante hardware de reset. No hay bootloader SPI.

Constantes finales: 30.000.000, 1.000.000 y 10.000.000 ciclos a 10 MHz.
`generate_game.py --sim` produce 300/100/1000 para simulación, nunca para el GDS.
La fuente original contenía una espera real de 250.000.000 ciclos; se preservó
y se documentó la discrepancia. El Makefile FPGA original sigue disponible,
pero el game.s actual tiene constantes de 10 MHz y no de 25 MHz.

## Síntesis y comparación RTL/netlist

```bash
bash scripts/hier_batch.sh
/opt/proyecto3-tools/librelane-3.0.17.AppImage python3 scripts/synth_hierarchy.py 0 --sim
/opt/proyecto3-tools/librelane-3.0.17.AppImage python3 scripts/synth_hierarchy.py 1 --sim
python3 scripts/gate_verify.py A_sim_hier
python3 scripts/gate_verify.py B_sim_hier
```

El último comando ejecuta realmente celdas GF180 sin SDF. Se retiran únicamente
los bloques specify de una copia temporal del modelo de celdas, debido a las
rutas ifnone no admitidas por Icarus. La simulación compara estímulos por ciclo
y trazas de respuestas; el timing se verifica aparte con STA/SPEF. Las ondas
seleccionadas se conservan comprimidas en results/functional/waves/.

## Flujos, barridos y corrida final

```bash
bash scripts/run_flow.sh asic/configs/A_p100_u30.json A_$(date -u +%Y%m%dT%H%M%SZ)
bash scripts/run_flow.sh asic/configs/B_p100_u30.json B_$(date -u +%Y%m%dT%H%M%SZ)
bash scripts/experiment_batch.sh A_p100_u40 A_p80_u40 A_p60_u40 A_p50_u40 A_p100_u50
bash scripts/run_flow.sh asic/configs/A_opt_p100_u40.json OPT_$(date -u +%Y%m%dT%H%M%SZ)
make -f Makefile.asic final
python3 scripts/collect_results.py
python3 scripts/archive_evidence.py
```

Final: **100 ns, 40 %, GF180MCU D y LibreLane**. No se desactivaron DRC, LVS,
antena ni setup/hold. El PDK no configura KLAYOUT_DRC_RUNSET y el flujo lo
advierte; el DRC reportado corresponde a Magic y al router. Se conservan advertencias de slew, fanout y capacitancia, detalladas en docs/RESULTADOS_MEDIDOS.md, que requieren revisión si se integra/fabrica.

Las corridas v1 aplanan temprano; v2 usa deferred_flatten y contador separado.
No combinar sus cifras sin identificar la versión. Snapshots/ZIP y hashes en
results/snapshots; configuración efectiva en results/runs/*/resolved.json.
Los barridos se vuelven a implementar; no se extrapolan slacks de una sola
corrida. La frecuencia se calcula con el menor período observado que cierre
todos los corners, distinguiéndolo del óptimo continuo no demostrado.

## Resultados y documentación

RTL A/B y netlists A/B reprodujeron diez aciertos, 136 ciclos por respuesta,
acumulado de 1.360, error preservando rondas y reset/reinicio. El final de A,
final_A_v2_p100_u40, tiene GDS real a 100 ns/40 %, DRC Magic/LVS/antena cero
y timing limpio en nueve corners. B_p100_u30_v2_resume_20261102T153658Z también
cierra esos criterios a 100 ns/30 %. Se compara con A_p100_u30_v2_resume bajo
los mismos 100 ns/30 %: los límites medidos sobre layout fijo son 57 ns para A
(17,543860 MHz) y 91 ns para B (10,989011 MHz), con fallo a 1 ns menos en cada
caso. [Reproducir la reanudación de B](docs/REPRODUCIR_B.md).

Los intentos B al 40 %, incluido el desvío físico local, permanecen como pruebas
incompletas y no se presentan como signoff aprobado. La comparación seleccionada
usa 30 % en ambas arquitecturas; el final obligatorio de A conserva el 40 %.
La síntesis jerárquica comparable midió A 147.741,3504 µm² y
B 613.575,9616 µm²; no confundir con áreas LibreLane o posteriores a filler.
Resultados posteriores y estado final: results/summary.csv.

[Informe](docs/Informe_Proyecto3.pdf), [migración](docs/MIGRACION_ASIC.md).

El informe se redactó en Google Docs y se exportó a PDF. `make -f Makefile.asic report`
(scripts/build_documents.py, requiere matplotlib) regenera los gráficos de docs/figures/
a partir de los datos curados incluidos en Git, sin carpetas temporales de las corridas.
Ejecutar `make -f Makefile.asic collect` solo cuando se quiera actualizar las tablas
desde corridas locales terminadas.
El [índice de evidencias](docs/EVIDENCIAS.md) relaciona cada resultado con sus archivos.
`.gitattributes` fija los finales de línea de las fuentes medidas y las
evidencias para conservar sus hashes al publicar y clonar desde Windows/Linux.

Resultados actualizados: [tablas medidas](docs/RESULTADOS_MEDIDOS.md). El layout final fijo pasa 59 ns y falla 58 ns: 16,949153 MHz observados; la entrega utiliza 100 ns. El game.hex original sí contenía 75.000.000 ciclos, a diferencia del game.s posterior de main; ver results/environment/original_program_consistency.json.
