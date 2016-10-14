
$(".startbtn").click(function(){
    $("#result").html("");        
    var script_name=$(this).data('script');
    $("#"+script_name+"_status").html(makelabel('info', 'running...'));
    var options=$("#"+script_name+"_options")[0].value;
    var file=$("#"+script_name+"_file")[0].value;
    var data = {script_name:script_name,
                options:options,
                file:file}
    var fdata = new FormData();
    fdata.append('file', $("#"+script_name+"_file")[0].files[0])

    console.log(file);
    if (file != ''){
        $("#"+script_name+"_status").html(makelabel('info', 'uploading...'));
        $.ajax({
                type : 'POST',
                url : "/upload",
                data:fdata,
                contentType: false,
                processData: false,
        }).done(function(){
            $("#"+script_name+"_status").html(makelabel('success', 'upload done'));
            console.log('Upload Done');
            ajax_call_start(script_name, data);
        }).fail(function(xhr, status, error){
            $("#"+script_name+"_status").html(makelabel('danger', 'upload error'));
            console.log(xhr.responseText);
        });
    }else{
        ajax_call_start(script_name, data);
    }
});

function ajax_call_start(script_name,data){
    $("#"+script_name+"_status").html(makelabel('info', 'running...'));
    $.ajax({
            url : "/start",
            dataType   : 'json',
            contentType: 'application/json; charset=UTF-8',
            data:JSON.stringify(data),
            type       : 'POST'
    }).done(function(data){
        $("#"+script_name+"_status").html(makelabel('success', 'done'));
        console.log(data);
        if ('output' in data){
            $("#result").html(data.output);        
        }
    }).fail(function(jqXHR, textStatus, errorThrown){
        window.res=jqXHR
        console.log(jqXHR.responseText);
        var response_obj=JSON.parse(jqXHR.responseText)
        $("#"+script_name+"_status").html(makelabel('danger', 'error'));
            $("#result").html(response_obj.output+"<br />"+response_obj.error);        
    });
}
function makelabel(my_class, text){
    return '<span class="label label-'+my_class+' lb-lg" >'+text+'</span>';
}
