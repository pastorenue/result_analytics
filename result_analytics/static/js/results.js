//Main App
$(document).ready(function(){
    //Use ajax to get the various data
    $('#cd-container').delegate('#new-data', 'click', function(e){
        e.preventDefault();
        $('#new-data').addClass('loader');
        $.get($(this).attr('href'), function(data){
            $('#cd-body').append(data);
            $('#new-data').hide();
        });
        });
    
     $('#cd-container').delegate('#new-data', 'click', function(e){
        e.preventDefault();
        $('#new-data').addClass('loader');
        var that =  $(this);
        $.get($(this).attr('href'), function(data){
            $('#new-data').hide();
            that.parent().parent(),remove();
            $('#cd-body').append(data);
        });
        });
     
     $('#cd-container').delegate('#new-data', 'submit', function(e){
        e.preventDefault();
        var form =  $('#data-form');
        var url = form.attr('action');
        $.post(url, form.serialize(), function(data){
            if (data.find('.errorlist').html()) {
                $('#new-data').hide();
                $('#cd-body').append(data);
            }
            else{
                $('#cd-table tr:last').after(data);
                $('#new-data').show();
            }
        });
        $(this).remove();
        });
    });
