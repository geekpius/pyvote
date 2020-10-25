$("#formLogin").on("submit", function(e){
    e.stopPropagation();
    var $this = $(this);
    var valid = true;
    $('#formLogin input').each(function() {
        let $this = $(this);
        
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('name').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if(valid){
        $(".btnLogin").html('<i class="fa fa-spin fa-spinner"></i> Signing...').attr('disabled',true);
        return true;
    }
    return false;
});


$("#formSignUp").on("submit", function(e){
    e.stopPropagation();
    var $this = $(this);
    var valid = true;
    $('#formLogin input').each(function() {
        let $this = $(this);
        
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('name').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if(valid){
        $(".btnSignUp").html('<i class="fa fa-spin fa-spinner"></i> Signing Up...').attr('disabled',true);
        return true;
    }
    return false;
});



$("#formReset").on("submit", function(e){
    e.stopPropagation();
    var $this = $(this);
    var valid = true;
    $('#formReset input').each(function() {
        let $this = $(this);
        
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('name').replace(/[\_]+/g, ' ')+' field is required');
        }
    });

    if(valid){
        $(".btnReset").html('<i class="fa fa-spin fa-spinner"></i> Reseting Password...').attr('disabled',true);
        return true;
    }
    return false;
});


//remove error message if inputs are filled
$("input").on('input', function(){
    if($(this).val()!=''){
        $(this).parents('.validate').find('.mySpan').text('');
    }else{ $(this).parents('.validate').find('.mySpan').text('The '+$(this).attr('name').replace(/[\_]+/g, ' ')+' field is required'); }
});


function getCaps(field){
    var valField = document.getElementById(field).value;
    document.getElementById(field).value=valField.toUpperCase();
}
