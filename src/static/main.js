async function consultar() {
    const pregunta = document.getElementById('pregunta').value;
    const res = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: pregunta })
    });

    const data = await res.json();
    const respuesta = data.response || 'Error al obtener respuesta';
    const tiempo = data.tiempo ? `\n⏱️ Tiempo: ${data.tiempo}` : '';

    document.getElementById('respuesta').innerText = respuesta + tiempo;
    document.getElementById('preguntaReescrita').innerText = data.pregunta_reescrita || '';

    await cargarHistorial();
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formularioSubida");
    if (form) {
        form.addEventListener("submit", async function (e) {
            e.preventDefault();
            const fileInput = document.getElementById("file");
            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            const resultado = document.getElementById("resultadoSubida");
            const loader = document.getElementById("documentos-loading");
            loader.classList.remove("d-none");
            resultado.innerText = "📥 Procesando archivo, por favor espera...";

            const res = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const data = await res.json();
            resultado.innerText = data.message || data.error;
            await cargarDocumentos();
            loader.classList.add("d-none");
        });
    }

    cargarDocumentos();
    cargarHistorial();
});

async function cargarDocumentos() {
    const res = await fetch("/documentos/lista");
    const data = await res.json();
    const ul = document.getElementById("listaDocumentos");
    ul.innerHTML = "";
    data.documentos.forEach(doc => {
        const li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center";
        li.innerHTML = `
            ${doc}
            <div>
                <button class="btn btn-sm btn-secondary me-2" onclick="reindexarDocumento('${doc}')">Reindexar</button>
                <button class="btn btn-sm btn-danger" onclick="eliminarDocumento('${doc}')">Borrar</button>
            </div>
        `;
        ul.appendChild(li);
    });
}

async function cargarHistorial() {
    const res = await fetch("/historial");
    const data = await res.json();
    const ul = document.getElementById("historial");
    ul.innerHTML = "";
    data.historial.reverse().forEach(item => {
        const li = document.createElement("li");
        li.className = "list-group-item";
        li.innerHTML = `<strong>❓ ${item.pregunta}</strong><br>🧠 ${item.respuesta}`;
        ul.appendChild(li);
    });
}

async function eliminarDocumento(nombre) {
    if (!confirm(`¿Seguro que deseas eliminar el archivo y su vectorización?\n${nombre}`)) return;

    const res = await fetch("/delete", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre })
    });
    const data = await res.json();
    alert(data.message);
    cargarDocumentos();
}

async function reindexarDocumento(nombre) {
    const res = await fetch("/reindex", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre })
    });
    const data = await res.json();
    alert(data.message);
    cargarDocumentos();
}