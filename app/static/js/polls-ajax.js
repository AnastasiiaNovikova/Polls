/**
 * Created by an.novikova on 09.04.18.
 */

$(document).ready( function(){
    $('.choose').click(function(){
        // var pollid;
        choice_id = $(this).attr("data-choiceid");
        console.log(choice_id);
        $.post('/app/choose/', {choice_id: choice_id}, function(data){
            // $('#count').html(data);
            $('#choose').hide();

        });
    });

});