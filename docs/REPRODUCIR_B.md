# Reproducción de la implementación física B seleccionada

La comparación utiliza A_p100_u30_v2_resume y
B_p100_u30_v2_resume_20261102T153658Z: 100 ns, 30 % inicial, GF180MCU D,
misma biblioteca, programa y orden de routing predeterminado, seis threads.
El final obligatorio de A permanece a 100 ns y 40 %.

La corrida B se reanudó desde un snapshot guardado durante una pausa. Para
reproducir esa entrada sin depender de las carpetas temporales del computador,
se incluye un único paquete:

`results/checkpoints/B_p100_u30_v2_resume_20261102T153658Z.zip`

Contiene diez vistas de entrada, un estado portable y un manifiesto con sus
hashes. No incluye el PDK ni las herramientas. El ZIP ocupa 16.740.963 bytes;
SHA256: `47ea624cdeffd18455ce0a210ee133ee227cf286b221457b538d4bca3ca9b528`.
La restauración ya se ejecutó y comprobó todos los hashes; respaldo:
`results/environment/B_checkpoint_restore_verification.log`.

## Desde un clon nuevo, en Ubuntu/WSL

Instalar las versiones fijadas siguiendo el README. Desde la raíz del proyecto:

```bash
python3 scripts/restore_checkpoint.py results/checkpoints/B_p100_u30_v2_resume_20261102T153658Z.zip
bash scripts/run_flow.sh asic/configs/B_p100_u30.json B_reproduccion_$(date -u +%Y%m%dT%H%M%SZ) --from OpenROAD.DetailedRouting -i "$PWD/work/restored_B_p100_u30_v2_resume_20261102T153658Z/state.json"
```

El restaurador valida también el hash de la configuración antes de escribir
el estado. OpenROAD recupera los cables del ODB y reinicia su optimización;
no se afirma una continuación idéntica del proceso interrumpido ni identidad
binaria de una nueva ejecución. El resultado debe volver a pasar DRC Magic,
LVS, antena y STA en los nueve corners.

Para implementar B desde RTL, sin usar el checkpoint:

```bash
bash scripts/run_flow.sh asic/configs/B_p100_u30.json B_desde_RTL_$(date -u +%Y%m%dT%H%M%SZ)
```

La frecuencia se caracteriza después de obtener el layout:

```bash
python3 scripts/characterize_fixed_layout.py NOMBRE_DE_LA_NUEVA_CORRIDA
```

Las mediciones incluidas pasan a 91 ns y fallan a 90 ns: 10,989011 MHz con
resolución de 1 ns, manteniendo layout, SPEF y retardos externos absolutos.
Esto no sustituye un barrido de síntesis/PnR. Los límites eléctricos adicionales
de slew, fanout y capacitancia permanecen declarados en el informe.
