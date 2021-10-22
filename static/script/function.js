function saltar(e, id) {
    (e.keyCode) ? k = e.keyCode : k = e.which;
    if (k == 13) { document.getElementById(id).focus(); }
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

    if (letras.indexOf(tecla) == -1 && !tecla_especial) { return false; }
}

function soloNumeros(e) {
    var key = window.event ? e.which : e.keyCode;
    if (key < 48 || key > 57) { e.preventDefault(); }
}

function seleccionar(id) {
    var val = $("#" + id).val();
    var can = val.length;
    document.getElementById(id).setSelectionRange(0, can);
}

function Nuevo() { location.reload(); }

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