// select option style
$('.select2').select2();
$('.select3').select2();

// get cash transaction
const getSaleTable = url => {
    $.ajax({
        url: url,
        type: "GET",
        success: function(response){
            $(".table-responsive").html(response);
        },
        error: function(response){
            console.log(JSON.stringify(response));
        }
    });
}


getSaleTable($(".table-responsive").data('href'));

// clear date selection on item select
$("#item").on("change", function(){
    if($("#index").val()!=''){
        $("#index").val('').trigger('change');
    }
    return false;
});


// date type select
$("#index").on("change", function(){
    var $this = $(this);
    if($("#item").val()==''){
        getSaleTable($(".table-responsive").data('href'));
    }else if($this.val()!=""){
        if($this.val()=="5"){
            $("#formSearchRange input[name='index']").val("5");
            $("#formSearchRange input[name='item_code']").val($("#item").val());
            $("#dateRangeModal").modal();
        }else{
            let data = {
                csrfmiddlewaretoken: $(".table-responsive").data("token"),
                item_code: $("#item").val(),
                index: $this.val(),
            }
            $.ajax({
                url: $(".table-responsive").data("href"),
                type: "POST",
                data: data,
                success: function(response){
                    $(".table-responsive").html(response);
                },
                error: function(response){
                    console.log(JSON.stringify(response));
                }
            });
        }
    }
    return false;
});



// filter between two dates
$("#formSearchRange").on("submit", function(e){
    e.preventDefault();
    e.stopPropagation();
    var valid = true;
    var $this = $(this);
    $('#formSearchRange input').each(function() {
        let $this = $(this);
        if(!$this.val()) {
            valid = false;
            $this.parents('.validate').find('.mySpan').text('The '+$this.attr('name').replace(/[\_]+/g, ' ')+' field is required');
        }
    });
    if(valid) {
        $('.btnFilterRange').html('<i class="fa fa-spinner fa-spin"></i> FILTERING...').attr('disabled', true);
        let data = $this.serialize();
        $.ajax({
            url: $this.attr("action"),
            type: "POST",
            data: data,
            success: function(response){
                $(".table-responsive").html(response);
                $("#dateRangeModal").modal("hide");
                $("#formSearchRange #start_date").val("");
                $("#formSearchRange #end_date").val("");
                $('.btnFilterRange').html('<i class="fa fa-search"></i> FILTER').attr('disabled', false);
                $("#index").val('').trigger('change');
            },
            error: function(response){
                console.log(JSON.stringify(response));
                $('.btnFilterRange').html('<i class="fa fa-search"></i> FILTER').attr('disabled', false);
            }
        });
    }
    return false;
});





