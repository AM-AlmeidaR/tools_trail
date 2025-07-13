document.addEventListener("DOMContentLoaded", function () {
    var canvas = document.getElementById("signature-pad");
    var clearButton = document.getElementById("clear-signature");
    var signatureDataInput = document.getElementById("signature-data");

    if (canvas) {
        var signaturePad = new SignaturePad(canvas, {
            backgroundColor: 'white', // Fondo blanco
            penColor: 'black' // Color del lápiz
        });

        // Borrar la firma
        clearButton.addEventListener("click", function () {
            signaturePad.clear();
        });

        // Guardar la firma en el input hidden antes de enviar el formulario
        document.querySelector("form").addEventListener("submit", function (e) {
            if (signaturePad.isEmpty()) {
                alert("Debe firmar antes de enviar el formulario.");
                e.preventDefault();
            } else {
                signatureDataInput.value = signaturePad.toDataURL();
            }
        });
    } else {
        console.error("No se encontró el canvas de firma.");
    }
});

