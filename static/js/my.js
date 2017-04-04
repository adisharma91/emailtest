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

    $('.imgbutton').click(function(e){
        $.get('/imgupload/',function(response){
            if(response != null){
                $('#lightbox_content').empty();
                $('#lightbox_content').html(response);
                $('#lightbox').css('display','inline');
            }
        })
    })

})

function closeModal() {
  document.getElementById('lightbox').style.display = "none";
}
