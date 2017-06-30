$(function(){
   $('#accordion').accordion(); 
});

$("button.delete").click(function(e){
   e.preventDefault();
   var id = $(this).attr('id');
   $.get({
      url: {% url 'photos:photos_delete' %},
      data: {'id': id},
      success: function(){
      
      }
   });
});