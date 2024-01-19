// Ajax para comodos
$("#search").keyup(function(){
    var p = $("input[id='search']").val();
    $.getJSON("http://localhost:8000/valim/imovel/servico/json/search?s=" + p, function(data){
        $("#select").empty();
        $("#select").append(
            $("<select id='lista'></select>")
        );
        $("#lista").append(
            $("<option selected></option>").text("Escolha uma opção")
        );
        for(var i = 0; i < data.length; i++){
            $("#lista").append(
                $("<option onclick='salvar(" + data[i].id + ")' value=''></option>").text(data[i].nome)
            );
        }
    })
});

function salvar(arg){
    $("input[id='comodo']").val(arg);
}
