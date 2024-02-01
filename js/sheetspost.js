async function crearTrabajo(contenido) {
  // Obtener la longitud de listaobjetos
  const numObjetos = contenido.listaobjetos.length;
  // Crear un array de updates para cada objeto en listaobjetos
  const updates = contenido.listaobjetos.map((objeto, index) => [
    parseInt(localStorage.getItem("maxid"))+index+1,
    contenido.ordenTrabajo,
    contenido.nombreProyecto,
    contenido.descripcionTrabajo,
    contenido.operariosdeTrabajo,
    contenido.areadeTrabajo,
    objeto.id, // Reemplaza 'dato1' con el nombre real del primer dato en objeto
    objeto.canti, // Reemplaza 'dato2' con el nombre real del segundo dato en objeto
    contenido.fechainicioTrabajo,
    new Date().toISOString(),
  ]);
  // Obtener la fila a editar
  const filaAEditar =2;
  // Actualizar la hoja de cálculo para cada objeto en listaobjetos
  for (let i = 0; i < numObjetos ; i++) {
    const response = await gapi.client.sheets.spreadsheets.values.append({
      spreadsheetId: SPREADSHEET,
      range: `${hoja}!A${parseInt(filaAEditar) + i}:j${parseInt(filaAEditar) + i}`,
      values: [updates[i]],
      valueInputOption: "USER_ENTERED",
    });
    // Puedes hacer algo con la respuesta si lo necesitas
    console.log(`Actualización para objeto ${i + 1}: `, response);
  }

  // location.reload();
  // Puedes devolver alguna información si es necesario
  return 'Actualizaciones completadas';

}
