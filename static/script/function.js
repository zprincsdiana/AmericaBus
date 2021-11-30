$(document).ready(function () {
    $('.destino').click(function () {
        console.log('hola mundo')
    })

    var cont = 0;

    let precio = $("#precio").text();
    precio_base = precio

    $(document).on("change", "#seleccionado", function () {
        if ($(this).prop('checked') == true) {
            cont++;
            console.log(cont);
            if (cont == 1) {
                precio = parseInt(precio);
            } else {
                precio = parseInt(precio) + parseInt(precio_base);
            }
            $("#precio").html(precio)
        } else {
            cont--;
            console.log(cont);
            if (cont <= 0) {
                precio = parseInt(precio);
            } else {
                precio = parseInt(precio) - parseInt(precio_base);
            }
            $("#precio").html(precio)
        }

        if (cont == 0) {
            $("#asientos_confirm").prop('disabled', true);
        } else {
            $("#asientos_confirm").prop('disabled', false);
        }
    })
    if (cont == 0) {
        $("#asientos_confirm").prop('disabled', true);
    }
    $("#ModalDeposito").keyup(function () {
        $("#ModalNuevoSaldo").val('');

        var saldo = $("#ModalSaldo").val();
        var deposito = $(this).val();

        if (deposito == '') {
            $("#ModalNuevoSaldo").val(saldo);
        } else {
            var NuevoSaldo = parseFloat(saldo) + parseFloat(deposito);
            var floatSaldo = parseFloat(NuevoSaldo);
            $("#ModalNuevoSaldo").val(floatSaldo);
        }
    })
});

function saltar(e, id) {
    (e.keyCode) ? k = e.keyCode : k = e.which;
    if (k == 13) {
        document.getElementById(id).focus();
    }
}

$('body').scrollspy({ target: '#navbar-example' })

function saltarselect(e) {
    $(".miClase").keypress(function (e) {
        if (e.which == 13) {
            var a = e.target.nextElementSibling;
            a.focus();
            console.log(a.innerHTML);
        }
    });
}

function soloLetras(e) {
    key = e.keyCode || e.which;
    tecla = String.fromCharCode(key).toLowerCase();
    letras = " áéíóúabcdefghijklmnñopqrstuvwxyz";
    especiales = "8-37-39-46";

    tecla_especial = false
    for (var i in especiales) {
        if (key == especiales[i]) {
            tecla_especial = true;
            break;
        }
    }

    if (letras.indexOf(tecla) == -1 && !tecla_especial) {
        return false;
    }
}

function soloNumeros(e) {
    var key = window.event ? e.which : e.keyCode;
    if (key < 48 || key > 57) {
        e.preventDefault();
    }
}

function seleccionar(id) {
    var val = $("#" + id).val();
    var can = val.length;
    document.getElementById(id).setSelectionRange(0, can);
}

function Nuevo() {
    location.reload();
}

function abrirPantalla() {
    var idusu = getParameterByName('idusu')
    $("#Idusu").val(idusu);
}

function buscarPasajero() {
    var IdBusqueda = $("#IdBusqueda").val();
    console.log("id a buscar: " + IdBusqueda);
    $.ajax({
        url: '/buscarPasajeroPorId?IdPasajero=' + IdBusqueda,
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $.each(data, function (i, e) {
                $("#IdPasajero").val(e.Id);
                $("#NombrePasajero").val(e.Nombre + ' ' + e.Paterno + ' ' + e.Materno);
            });
        }
    });
}

function llenarTablaAdmin() {
    $("#tbody_ListaCuentas").empty();
    $.ajax({
        url: '/ListarUsuarios',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $.each(data, function (i, e) {
                if (e.id_estado == 0) {
                    var visible = ''
                } else {
                    var visible = 'none'
                }
                $("#tbody_ListaCuentas").append('<tr>' +
                    '<td>' + e.id_usuario + '</td>' +
                    '<td>' + e.nombre + '</td>' +
                    '<td>' + e.apellido_paterno + '</td>' +
                    '<td>' + e.apellido_materno + '</td>' +
                    '<td>' + e.dni + '</td>' +
                    '<td>' + e.estado + '</td>' +
                    '<td style="display:' + visible + '"><button class="btn-outline-warning" onclick=ListarDepartamentos();EnviarDatosEditar(' + e.id_usuario + '); data-toggle="modal" data-target="#ModalEditar"><i class="far fa-edit"></i></button>' +
                    '  <button class="btn-outline-danger" onclick=EliminarUsuarioPorId(' + e.id_usuario + ');><i class="far fa-trash-alt"></i></button></td>' +
                    '</tr>')
            });
            //location.href ="http://127.0.0.1:3000/administrar"


        }
    });
}

function BuscarUsuario() {
    $("#tbody_ListaCuentas").empty();
    var nombre = $("#NombreUsuario").val();
    var dni = $("#DniUusario").val();

    if (dni.length != 0 && nombre.length != 0) {
        $.ajax({
            url: '/ListarUsuarioPorNombreDni?nombre=' + nombre + '&dni=' + dni + '&opt=' + 1,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $.each(data, function (i, e) {
                    $("#tbody_ListaCuentas").append('<tr>' +
                        '<td>' + e.id_usuario + '</td>' +
                        '<td>' + e.nombre + '</td>' +
                        '<td>' + e.apellido_paterno + '</td>' +
                        '<td>' + e.apellido_materno + '</td>' +
                        '<td>' + e.dni + '</td>' +
                        '<td>' + e.estado + '</td>' +
                        '<td><button class="btn-outline-warning" onclick=ListarDepartamentos();EnviarDatosEditar(' + e.id_usuario + '); data-toggle="modal" data-target="#ModalEditar"><i class="far fa-edit"></i></button>' +
                        '  <button class="btn-outline-danger" onclick=EliminarUsuarioPorId(' + e.id_usuario + ');><i class="far fa-trash-alt"></i></button></td>' +
                        '</tr>')
                });
            }
        });
    } else if (dni.length == 0 && nombre.length != 0) {
        $.ajax({
            url: '/ListarUsuarioPorNombreDni?nombre=' + nombre + '&dni=' + dni + '&opt=' + 2,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $.each(data, function (i, e) {
                    $("#tbody_ListaCuentas").append('<tr>' +
                        '<td>' + e.id_usuario + '</td>' +
                        '<td>' + e.nombre + '</td>' +
                        '<td>' + e.apellido_paterno + '</td>' +
                        '<td>' + e.apellido_materno + '</td>' +
                        '<td>' + e.dni + '</td>' +
                        '<td>' + e.estado + '</td>' +
                        '<td><button class="btn-outline-warning" onclick=ListarDepartamentos();EnviarDatosEditar(' + e.id_usuario + '); data-toggle="modal" data-target="#ModalEditar"><i class="far fa-edit"></i></button>' +
                        '  <button class="btn-outline-danger" onclick=EliminarUsuarioPorId(' + e.id_usuario + ');><i class="far fa-trash-alt"></i></button></td>' +
                        '</tr>')
                });
            }
        });
    } else if (dni.length != 0 && nombre.length == 0) {
        $.ajax({
            url: '/ListarUsuarioPorNombreDni?nombre=' + nombre + '&dni=' + dni + '&opt=' + 1,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                $.each(data, function (i, e) {
                    $("#tbody_ListaCuentas").append('<tr>' +
                        '<td>' + e.id_usuario + '</td>' +
                        '<td>' + e.nombre + '</td>' +
                        '<td>' + e.apellido_paterno + '</td>' +
                        '<td>' + e.apellido_materno + '</td>' +
                        '<td>' + e.dni + '</td>' +
                        '<td>' + e.estado + '</td>' +
                        '<td><button class="btn-outline-warning" onclick=ListarDepartamentos();EnviarDatosEditar(' + e.id_usuario + '); data-toggle="modal" data-target="#ModalEditar"><i class="far fa-edit"></i></button>' +
                        '  <button class="btn-outline-danger" onclick=EliminarUsuarioPorId(' + e.id_usuario + ');><i class="far fa-trash-alt"></i></button></td>' +
                        '</tr>')
                });
            }
        });
    }
}

function EliminarUsuarioPorId(id_usuario) {
    console.log('EliminarUsuarioPorId');
    $.ajax({
        url: '/EliminarUsuarioPorId?id_usuario=' + id_usuario,
        dataType: 'json',
        success: function (data) {
            console.log(data);
            llenarTablaAdmin();
        }
    });
}

// function abrirModalEditar(id_usuario) {
//     setTimeout(EnviarDatosEditar(id_usuario), 1000);
// }

function EnviarDatosEditar(id_usuario) {
    $("#IdUsuEdit").val(id_usuario)
    LimpiarModalEditar();
    $.ajax({
        url: '/ListarUsuarioPorId?id_usuario=' + id_usuario,
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $.each(data, function (i, e) {
                $("#ModalNombre").val(e.nombre);
                $("#ModalPaterno").val(e.apellido_paterno);
                $("#ModalMaterno").val(e.apellido_materno);
                $("#ModalDNI").val(e.dni);
                $("#ModalFechaNacimiento").val(e.fecha_nacimiento);
                $("#ModalTelefono").val(e.telefono);
                $("#ModalDireccion").val(e.direccion);
                $("#ModalDepartamento").val(e.id_departamento);
                $("#ModalSaldo").val(e.saldo);
                $("#ModalNuevoSaldo").val(e.saldo);
            });
        }
    });
}

function ListarDepartamentos() {
    $.ajax({
        url: '/ListarDepartamentos?',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            $.each(data, function (i, e) {
                $("#ModalDepartamento").append('<option value="' + e.id_departamento + '" >' + e.nombre + '</option>')
            });
        }
    });
}

function EditarUsuario() {
    var id_usuario = $("#IdUsuEdit").val();
    var nombre = $("#ModalNombre").val();
    var paterno = $("#ModalPaterno").val();
    var materno = $("#ModalMaterno").val();
    var dni = $("#ModalDNI").val();
    var nacimiento = $("#ModalFechaNacimiento").val();
    var telefono = $("#ModalTelefono").val();
    var direccion = $("#ModalDireccion").val();
    var departamento = $("#ModalDepartamento").val();
    var nuevosaldo = $("#ModalNuevoSaldo").val();

    $.ajax({
        url: '/EditarUsuarioPorId?id_usuario=' + id_usuario + '&nombre=' + nombre + '&paterno=' + paterno + '&materno=' + materno +
            '&dni=' + dni + '&nacimiento=' + nacimiento + '&telefono=' + telefono + '&direccion=' + direccion + '&departamento=' + departamento +
            '&nuevosaldo=' + nuevosaldo,
        dataType: 'json',
        success: function (data) {
            EnviarDatosEditar(id_usuario);
        }
    });
}

let myChart;

function verEstadisticaAnio(anio) {
    var ctx = document.getElementById('myChart').getContext('2d');
    if (myChart) {
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            datasets: [{
                label: 'Importes Mensuales - Año '+anio,
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: ['black'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    })

    let url = 'http://127.0.0.1:3000/verEstadisticaPorAnio?anio=' + anio
    fetch(url)
        .then(response => response.json())
        .then(datos => mostrar(datos))
        .catch(error => console.log(error))

    const mostrar = (estadistica) => {
        estadistica.forEach(element => {
            myChart.data['labels'].push(element.mes)
            myChart.data['datasets'][0].data.push(element.importe)
        })
        myChart.update('active');
    }
}

function LimpiarModalEditar() {
    $("#ModalNombre").val('');
    $("#ModalPaterno").val('');
    $("#ModalMaterno").val('');
    $("#ModalDNI").val('');
    $("#ModalFechaNacimiento").val('');
    $("#ModalTelefono").val('');
    $("#ModalDireccion").val('');
    $("#ModalDepartamento").change();
    $("#ModalSaldo").val('');
    $("#ModalNuevoSaldo").val('');
    $("#ModalDeposito").val('');
}