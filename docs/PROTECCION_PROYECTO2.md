# Proyecto 2 permanece intacto

Se trabajó exclusivamente sobre el clon independiente `Proyecto3AC` dentro de
outputs. No se ejecutó ninguna operación de escritura contra GitHub de Proyecto 2.
Tampoco se ejecutaron commits o pushes en Proyecto3AC.

La consulta `git ls-remote` después de la advertencia del usuario confirmó:

- main: `67d0c48bcc115614a4029ff024277cb53bc30a05`
- dev-game: `6c0f7c69c656bc7226278f66ab4bd390bc12e820`

Ambas revisiones coinciden con las registradas al clonar. Evidencia:
`results/environment/proyecto2_remote_verified.txt`.

En el clon de Proyecto3AC, el remoto `proyecto2` conserva su URL de lectura y
tiene `pushurl=DISABLED`, como protección local adicional. `origin` apunta al
nuevo Proyecto3AC; añadir esa URL local no crea ni publica un repositorio remoto.
