$(document).ready(function(){
    $('.applybtn').click(function(e){
        e.preventDefault();
        var thisbtn =$(this)
        action = $(this).attr('data-href')
        $.post(action,$('#applyfrm').serialize(), function(response){
            if(response.status == true){
                thisbtn.html('Applied').attr('disabled','true');
            }
            else{
                thisbtn.html('Error').attr('disabled','true');
            }
        })
    })
})
