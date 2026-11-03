# Proyecto 3: Pochoco SoC de FPGA a ASIC

Arquitectura de Computadores 2026-2, Universidad de los Andes. Grupo 15: Martin Heiremans,
Felix Svensson y Juan Pablo Saavedra. Profesor: Jorge Gómez Mir.

El SoC y el juego de reflejos del Proyecto 2, llevados de RTL a GDSII con LibreLane y el PDK
GF180MCU. El informe está en [docs/Informe_Proyecto3.pdf](docs/Informe_Proyecto3.pdf).

## Versiones

| Herramienta | Versión |
| --- | --- |
| LibreLane | 3.0.17 (AppImage, SHA256 `c8ef5ae26b1fc53dd1dd30fe2f1a1da6ab0fdf471dd5a94c2b85d2b3db36833c`) |
| Yosys | 0.62 |
| OpenROAD | `dcf36133a369abc8f3c5e5738cd4d82e4903c0e0` |
| OpenSTA | `857316ff001b2a8dbbdc5996944d08a6d38c87ab` |
| Magic | 8.3.623 |
| Netgen | 1.5.316 |
| KLayout | 0.30.7 |
| PDK | GF180MCU, variante `gf180mcuD`, Open PDKs `54435919abffb937387ec956209f9cf5fd2dfbee` |
| Biblioteca de celdas | `gf180mcu_fd_sc_mcu7t5v0` |

## Instalación

Se usó Windows con WSL (Ubuntu 24.04). En PowerShell:

```powershell
wsl --install -d Ubuntu-24.04
```

En Ubuntu:

```bash
sudo apt update
sudo apt install -y curl uidmap locales libfuse2t64 iverilog python3 make git
sudo locale-gen en_US.UTF-8

sudo mkdir -p /opt/proyecto3-tools
sudo chown "$USER" /opt/proyecto3-tools
curl -fL -o /opt/proyecto3-tools/librelane-3.0.17.AppImage \
  https://github.com/librelane/librelane/releases/download/3.0.17/librelane-devshell-x86_64.AppImage
chmod +x /opt/proyecto3-tools/librelane-3.0.17.AppImage
sha256sum /opt/proyecto3-tools/librelane-3.0.17.AppImage   # debe coincidir con la tabla

# Descarga el PDK en /opt/proyecto3-tools/pdks y prueba la instalación
/opt/proyecto3-tools/librelane-3.0.17.AppImage librelane --pdk gf180mcuD \
  --pdk-root /opt/proyecto3-tools/pdks --smoke-test
```

## Regenerar el programa desde game.s

```bash
make -f Makefile.asic generate
```

Ensambla `sw/game.s` con las constantes para 10 MHz y deja en `asic/generated/` la ROM
(`program_rom.v`), los valores de reset de la memoria B (`program_reset.vh`) y `game.hex`.
Usa `assembler/assembler.py` con la opción `--rom-dir`.

Pruebas RTL de las dos memorias y del juego:

```bash
make -f Makefile.asic verify
```

## Corrida final

```bash
make -f Makefile.asic final
```

Usa `asic/configs/final.json`: 100 ns, 40 % de utilización y memoria A (ROM + RAM). El
resultado queda en `asic/configs/runs/final_<fecha>/`. La corrida entregada está en
`results/runs/final_A_v2_p100_u40/`, con el GDS en `views/gds/asic_top.gds`: DRC, LVS y
antena limpios, y timing cumplido en los 9 corners.

## Simulación post-síntesis

```bash
/opt/proyecto3-tools/librelane-3.0.17.AppImage python3 scripts/synth_hierarchy.py 0 --sim
python3 scripts/gate_verify.py A_sim_hier
```

Sintetiza el diseño con el programa acortado y simula el netlist con las celdas GF180, sin
retardos. Con `1` y `B_sim_hier` se prueba la memoria B.

## Carpetas

- `rtl/`: RTL original del Proyecto 2, sin cambios.
- `asic/rtl/`: RTL para ASIC. `asic/configs/`: configuraciones de LibreLane.
  `asic/constraints/pins.cfg`: ubicación de los terminales.
- `sw/game.s` y `assembler/`: programa del juego y assembler.
- `sim/`: testbenches.
- `results/`: evidencia de las corridas, con su índice en [docs/EVIDENCIAS.md](docs/EVIDENCIAS.md).
