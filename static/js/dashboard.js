/*
* JS DASHBOARD
*/
/* Oculta menu lateral */
$(document).ready(function(){
	$("#aside").hide();
	$("#section").addClass("col-md");
});

/* Exibe menu lateral */
$("#dash").click(function(){
	$("#aside").addClass("col-md-2");
	$("#aside").toggle("slow");
});

// Ajax para comodos
$("#sku").keyup(function(){
    var p = $("input[id='sku']").val();
    $.getJSON("http://localhost:8000/valim/default/servico/json/search?s=" + p, function(data){
        $("#skus").empty();
        $("#skus").append(
        );
        for(var i = 0; i < data.length; i++){
            $("#skus").append(
                $("<option />").text(data[i].sku)
            );
        }
    })
});
