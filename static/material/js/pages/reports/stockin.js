// get user stock table
const getStockDataTable = () => {
    $.ajax({
        url: $(".table-responsive").data('href'),
        type: "GET",
        success: function(response){
            $(".table-responsive").html(response);
        },
        error: function(response){
            console.log(JSON.stringify(response));
        }
    });
}

getStockDataTable();


// reload all stock
$(".btnReload").on("click", function(e){
    e.preventDefault();
    var $this = $(this);
    getStockDataTable();
    return false;
});


// filter range stock
$(".btnRange").on("click", function(e){
    e.preventDefault();
    $("#dateRangeModal").modal();
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
            url: $this.attr('action'),
            type: "POST",
            data: data,
            success: function(response){
                $(".table-responsive").html(response);
                $("#dateRangeModal").modal("hide");
                $("#dateRangeModal #start_date").val("");
                $("#dateRangeModal #end_date").val("");
                $('.btnFilterRange').html('<i class="fa fa-search"></i> FILTER').attr('disabled', false);
            },
            error: function(response){
                console.log(JSON.stringify(response))
                $('.btnFilterRange').html('<i class="fa fa-search"></i> FILTER').attr('disabled', false);
            }
        });
    }
    return false;
});


