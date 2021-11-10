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
});

function saltar(e, id) {
    (e.keyCode) ? k = e.keyCode : k = e.which;
    if (k == 13) {
        document.getElementById(id).focus();
    }
}

$('body').scrollspy({target: '#navbar-example'})

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
                    '<td style="display:' + visible + '"><button class="btn-outline-warning" onclick=EnviarDatosEditar(' + e.id_usuario + ');><i class="far fa-edit"></i></button>' +
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
                        '<td><button class="btn-outline-warning" onclick=EnviarDatosEditar(' + e.id_usuario + ');><i class="far fa-edit"></i></button>' +
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
                        '<td><button class="btn-outline-warning" onclick=EnviarDatosEditar(' + e.id_usuario + ');><i class="far fa-edit"></i></button>' +
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
                        '<td><button class="btn-outline-warning" onclick=EnviarDatosEditar(' + e.id_usuario + ');><i class="far fa-edit"></i></button>' +
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