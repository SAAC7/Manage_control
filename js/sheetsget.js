const hoja = "BD";
let trabajos;


async function getTrabajos() {
  let response;
  try {
    response = await gapi.client.sheets.spreadsheets.values.get({
      spreadsheetId: SPREADSHEET,
      range: hoja + "!A:J",
    });
  } catch (err) {
    console.error(err);
    return;
  }
  const range = response.result;
  if (!range || !range.values || range.values.length == 0) {
    console.warn("No se encontraron valores");
    return;
  }
  trabajos = [];
  let numfila = 1;
  range.values.forEach((fila) => {
    if (isNaN(parseInt(fila[0]))) return;
    const nuevosTrabajos = {
      id: fila[0],
      ordenTrabajo: fila[1],
      nombreProyecto: fila[2],
      descripcionTrabajo: fila[3],
      operariosdeTrabajo: fila[4],
      areadeTrabajo: fila[5],
      idproduccion: fila[6],
      cantidadproduccion: fila[7],
      fechainicioTrabajo: fila[8],
      horainicioTrabajo: fila[9],
      // fechafinTrabajo: fila[10],
      // horafinTrabajo: fila[11],
      // descripcionAtraso: fila[16],
      // estado: fila[17],
      // comentario: fila[18],
    };
    trabajos.push(nuevosTrabajos);
    numfila++;
  });
  // localStorage.removeItem('datos')
  localStorage.setItem("datos", JSON.stringify(trabajos));
}
async function getTrabajosporColaborador(colaborador) {
  colaborador = colaborador.toLowerCase();
  let response;
  try {
    response = await gapi.client.sheets.spreadsheets.values.get({
      spreadsheetId: SPREADSHEET,
      range: hoja + "!A:S",
    });
  } catch (err) {
    console.error(err);
    return;
  }
  const range = response.result;
  if (!range || !range.values || range.values.length == 0) {
    console.warn("No se encontraron valores");
    return;
  }
  trabajos = [];
  let numfila = 1;
  range.values.forEach((fila) => {
    if (isNaN(parseInt(fila[0]))) return;
    if (fila[4] == colaborador) {
      const nuevosTrabajos = {
        id: fila[0],
        ordenTrabajo: fila[1],
        nombreProyecto: fila[2],
        descripcionTrabajo: fila[3],
        operariosdeTrabajo: fila[4],
        areadeTrabajo: fila[5],
        idproduccion: fila[6],
        cantidadproduccion: fila[7],
        fechainicioTrabajo: fila[8],
        horainicioTrabajo: fila[9],
        fechafinTrabajo: fila[10],
        horafinTrabajo: fila[11],
        descripcionAtraso: fila[16],
        estado: fila[17],
        comentario: fila[18],
      };
      trabajos.push(nuevosTrabajos);
    }
    numfila++;
  });
  console.log(trabajos);
}
async function getTrabajosporArea(area) {
  area = area.toLowerCase();
  let response;
  try {
    response = await gapi.client.sheets.spreadsheets.values.get({
      spreadsheetId: SPREADSHEET,
      range: hoja + "!A:S",
    });
  } catch (err) {
    console.error(err);
    return;
  }
  const range = response.result;
  if (!range || !range.values || range.values.length == 0) {
    console.warn("No se encontraron valores");
    return;
  }
  trabajos = [];
  let numfila = 1;
  range.values.forEach((fila) => {
    if (isNaN(parseInt(fila[0]))) return;
    if (fila[5] == area) {
      const nuevosTrabajos = {
        id: fila[0],
        ordenTrabajo: fila[1],
        nombreProyecto: fila[2],
        descripcionTrabajo: fila[3],
        operariosdeTrabajo: fila[4],
        areadeTrabajo: fila[5],
        idproduccion: fila[6],
        cantidadproduccion: fila[7],
        fechainicioTrabajo: fila[8],
        horainicioTrabajo: fila[9],
        fechafinTrabajo: fila[10],
        horafinTrabajo: fila[11],
        descripcionAtraso: fila[16],
        estado: fila[17],
        comentario: fila[18],
      };
      trabajos.push(nuevosTrabajos);
    }
    numfila++;
  });
  return JSON.stringify(trabajos);
}
async function maxid(){
  let response;
  try {
    response = await gapi.client.sheets.spreadsheets.values.get({
      spreadsheetId: SPREADSHEET,
      range: hoja + "!A:A",
    });
  } catch (err) {
    console.error(err);
    return;
  }

  const range = response.result;
  if (!range || !range.values || range.values.length == 0) {
    console.warn("No se encontraron valores");
    return;
  }
  let maxId = 0;
  range.values.forEach((fila) => {
    const currentId = parseInt(fila[0]);
    if (!isNaN(currentId) && currentId > maxId) {
      maxId = currentId;
    }
  });
  // localStorage.removeItem('maxid')
  localStorage.setItem("maxid", JSON.stringify(maxId));
}
