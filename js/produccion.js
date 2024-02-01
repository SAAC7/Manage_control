let trabajoslocal;
function getTrabajosarea_local(area){
    area=area.toLowerCase();
    datos = JSON.parse(localStorage.getItem('datos'));
    // console.log(datos);
    trabajoslocal=[];
    datos.forEach((fila) => {
        if (isNaN(parseInt(fila.id))) return;
        if (fila.areadeTrabajo == area) {
            trabajoslocal.push(fila);
        }
      });
    //   return JSON.stringify(trabajos);
    return (trabajoslocal);
}

function insertarDatosEnTabla(datos, tablaId) {
  const tbody = document
    .getElementById(tablaId)
    .getElementsByTagName("tbody")[0];

  // Limpiar el tbody antes de insertar nuevos datos
  tbody.innerHTML = "";

  // Propiedades específicas que deseas mostrar en cada fila
  const propiedadesMostrar = [
    "id",
    "ordenTrabajo",
    "descripcionTrabajo",
    "operariosdeTrabajo",
    "idproduccion",
    "cantidadproduccion",
    "fechainicioTrabajo",
    "horainicioTrabajo",
  ];
  // Iterar sobre los datos y agregar filas a la tabla
  datos.forEach((fila) => {
    const nuevaFila = tbody.insertRow();
    propiedadesMostrar.forEach((propiedad) => {
      const celda = nuevaFila.insertCell();
      celda.innerHTML = fila[propiedad] || ""; // Si la propiedad no existe, coloca un valor predeterminado
    });

    // Agregar botones de opciones (eliminar y editar)
    const opcionesCell = nuevaFila.insertCell();
    opcionesCell.innerHTML = `
    <button class="btn btn-danger btn-icon-split btn-sm" onclick="finalizartarea(i)">Finalizar</button>

      `;
  });
}


// function actualizarTablas() {
    
// }
// finalizaredit.addEventListener("click",()=> finalizartarea(indiceSeleccionado))
// function finalizartarea(index){
    
// }