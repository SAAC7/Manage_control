let contadorFilas = 0;
let listaobjetos = [];

function cargarOperarios(areaSeleccionada) {
    // Obtén las opciones de operarios según el área seleccionada
    var operariosDisponibles = obtenerOperariosPorArea(areaSeleccionada);

    // Obtén el elemento select de operarios
    var selectOperarios = document.getElementById("operarios");

    // Elimina todas las opciones existentes en el select de operarios
    selectOperarios.innerHTML = "";

    // Agrega las nuevas opciones al select de operarios
    operariosDisponibles.forEach(function (operario) {
        var opcion = document.createElement("option");
        opcion.value = operario;
        opcion.text = operario;
        selectOperarios.appendChild(opcion);
    });
}
function obtenerOperariosPorArea(area) {
    // Implementa la lógica para obtener los operarios según el área
    // En este ejemplo, se utiliza un objeto para representar la relación entre áreas y operarios
  
    var operariosPorArea = {
      "trazo": ["Ceferino Pérez", "Ever Xiloj"],
      "cnccorte": ["William Cuzal JR", "Helaman Sacalxot", "Juan Carlos Sajche"],
      "postformado": ["Geovanni López"],
      "armado": ["Amilcar Leiva", "Ervin Can", "Ceferino Pérez", "José Coyoy", "Maynor Pérez", "Selvin Hernández"]
    };
  
    return operariosPorArea[area] || [];
  }
function validarFormulario() {
  // Obtén los valores de los campos
  var ordenTrabajo = document.getElementById("ordenTrabajo").value;
  var descripcionTrabajo = document.getElementById("descripcionProducto").value;
  var fechainicioTrabajo = document.getElementById("fechaInicioProyecto").value;
  // ... (otros campos)

  // Realiza la validación de campos requeridos
  if (
    ordenTrabajo === "" ||
    descripcionTrabajo === "" ||
    fechainicioTrabajo === ""
  ) {
    alert("Por favor, complete todos los campos requeridos.");
    return false; // Evita que el formulario se envíe si falta algún dato
  }

  // Continúa con la lógica de envío de datos si todos los campos están llenos
  // ...
  console.log("envio de datos");
  enviarDatos();
  console.log("envio de datos2");
  return true; // Permite que el formulario se envíe si todos los campos están llenos
}
function habilitarBotonEnvio() {
  var botonEnvio = document.getElementById("botonEnvio");
  botonEnvio.disabled = contadorFilas === 0;
}

function eliminarFila(button) {
  var row = button.parentNode.parentNode;
  var rowIndex = row.rowIndex;

  // Obtener el id y cantidad del mueble de la fila que se va a eliminar
  var idMuebleEliminar =
    document.getElementById("tablaProduccion").rows[rowIndex].cells[0]
      .innerHTML;
  var cantidadEliminar =
    document.getElementById("tablaProduccion").rows[rowIndex].cells[1]
      .innerHTML;

  // Eliminar la fila de la tabla
  row.parentNode.removeChild(row);

  // Encontrar el índice del objeto que queremos eliminar
  var indexEliminar = listaobjetos.findIndex(function (producto) {
    return (
      producto.id === idMuebleEliminar && producto.canti === cantidadEliminar
    );
  });

  // Eliminar solo un elemento específico de la listaobjetos
  if (indexEliminar !== -1) {
    listaobjetos.splice(indexEliminar, 1);
  }

  // Decrementar el contador de filas
  contadorFilas--;

  // Habilitar/deshabilitar el botón de envío según sea necesario
  habilitarBotonEnvio();
}
function agregarFilaTabla() {
  // Obtener los valores de los campos
  var idMueble = document.getElementById("idMueble").value;
  var cantidad = document.getElementById("idcantidad").value;

  // Validar que los campos no estén vacíos
  if (idMueble === "" || cantidad === "") {
    alert("Por favor, complete todos los campos.");
    return;
  }
  // Crear lista con los datos

  const nuevoProducto = {
    id: idMueble,
    canti: cantidad,
  };
  listaobjetos.push(nuevoProducto);
  // Agregar una nueva fila a la tabla
  var table = document.getElementById("tablaProduccion");
  var newRow = table.insertRow(table.rows.length);
  // Insertar celdas con los valores obtenidos
  var cell1 = newRow.insertCell(0);
  var cell2 = newRow.insertCell(1);
  var cell3 = newRow.insertCell(2);

  cell1.innerHTML = idMueble;
  cell2.innerHTML = cantidad;
  cell3.innerHTML = "<button onclick='eliminarFila(this)'>Eliminar</button>";

  // Incrementar el contador de filas
  contadorFilas++;

  // Limpiar los campos después de agregar la fila
  document.getElementById("idMueble").value = "";
  document.getElementById("idcantidad").value = "";

  // Habilitar el botón de envío si hay al menos una fila
  habilitarBotonEnvio();
}
function actualizarOperarios(operarios) {
  var operariosSelect = document.getElementById("operarios");
  operariosSelect.innerHTML = ""; // Limpiar opciones existentes

  // Agregar nuevas opciones
  operarios.forEach(function (operario) {
    var option = document.createElement("option");
    option.value = operario;
    option.text = operario;
    operariosSelect.appendChild(option);
  });
}


function enviarDatos() {
    // Aquí puedes construir un objeto con todos los datos que deseas enviar al servidor
  var datosAEnviar = {
    ordenTrabajo: document.getElementById("ordenTrabajo").value,
    nombreTrabajo: document.getElementById("nombreProyecto").value,
    descripcionTrabajo: document.getElementById("descripcionProducto").value,
    areadeTrabajo: document.getElementById("area").value,
    operariosdeTrabajo: document.getElementById("operarios").value,
    fechainicioTrabajo: document.getElementById("fechaInicioProyecto").value,
    // ... (otros datos)
    listaobjetos: listaobjetos  // Asegúrate de que listaobjetos esté disponible en este contexto
  };

  var jsonData = JSON.stringify(datosAEnviar);

  crearTrabajo(datosAEnviar)
  }

