$(document).ready(function () {

    $("#btn_buscar").click(function () {
        buscarPasajero();
    }).keyup(function (event) {
        if (event.keyCode == 13) {
            buscarPasajero();
        }
    });

    $("#IdBusqueda").keyup(function () {
        var IdBusqueda = $("#IdBusqueda").val();
        if (IdBusqueda.length < 1) {
            $("#NombrePasajero").val('');
        }
    });

});