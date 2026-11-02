# Publicación personal del alumno

No se ejecutaron commit ni push. Proyecto 2 permanece intacto. El perfil de
GitHub conectado devolvió FelixSvensson y fasvensson@miuandes.cl; se configuraron
únicamente en este clon de Proyecto3AC, sin alterar la configuración global.
También se activó `core.longpaths=true` solo en este clon para los nombres largos
de los reportes de STA en Windows.
`.gitattributes` conserva literalmente los bytes de archivos generados y
evidencias, y fuerza CRLF en los textos originales que se midieron con esos
bytes. Los scripts de shell conservan LF y los binarios no se convierten.
No cambiar esas reglas al publicar:
permiten conservar los hashes registrados en clones Windows y Linux.
Revisar y confirmar esa identidad antes de crear el commit personalmente.

La consulta al remoto Proyecto3AC devolvió Repository not found. El conector
disponible no permite crear repositorios vacíos. Crear manualmente
FelixSvensson/Proyecto3AC en GitHub, **sin README, licencia ni .gitignore inicial**,
para conservar la historia procedente de Proyecto 2 sin merges.

## Comandos en PowerShell (solo el alumno los ejecuta)

```powershell
Set-Location 'C:\Users\Lenovo\Documents\Codex\2026-10-28\files-pasted-by-the-user-misi\outputs\Proyecto3AC'
git config --show-origin --get user.name
git config --show-origin --get user.email
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
git branch --show-current
git remote -v
git config --local --get core.longpaths
git status --short
```

El nombre esperado es FelixSvensson, correo fasvensson@miuandes.cl, rama main y
origin debe apuntar exclusivamente a Proyecto3AC. Si prefieres otro nombre real
o correo verificado de tu cuenta, cambia solo la configuración local antes del
commit, sin inventar direcciones.

Revisar docs/CHECKLIST_ENTREGA.md antes de publicar. Añadir los archivos correctos:

```powershell
git add .gitignore .gitattributes README.md Makefile.asic requirements-docs.txt assembler/assembler.py assembler/test_rom.py asic/ scripts/ sw/game.s sw/game.hex sw/game_fpga_original.s sim/asic_game_tb.v sim/asic_memory_tb.v sim/memory_equivalence_tb.v sim/generated/ docs/ results/
git diff --cached --stat
git diff --cached --check
git status --short
```

Las carpetas asic/configs/runs, caches, PDK, herramientas instaladas y VCD sin comprimir deben
estar ignoradas. Los GDS seleccionados, métricas, logs curados y ondas comprimidas
sí forman parte de la entrega. Inspeccionar la lista antes de continuar.

Crear personalmente el commit y publicar:

```powershell
git commit -m 'Proyecto 3: implementación ASIC de Pochoco SoC con LibreLane y GF180MCU'
git push -u origin main
git rev-parse HEAD
git ls-remote origin refs/heads/main
git status
Start-Process 'https://github.com/FelixSvensson/Proyecto3AC'
```

Las dos revisiones mostradas por rev-parse y ls-remote deben coincidir. El alumno
debe comprobar en GitHub que el informe PDF, guía, fuentes y evidencia aparecen.
No ejecutar ningún push hacia el remoto proyecto2, cuyo destino de escritura se
deshabilitó en este clon.
