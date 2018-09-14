$("#logout").click(function () {
    $.ajax({
        type: 'POST',
        url: '/gdisconnect',
        processData: false,
        contentType: 'application/octet-stream; charset=utf-8',
        success: function (result) {
            console.log(result);
            $('#result').html('<div class="row"><div class="text-center"><h2>Logout Successful !!</h2><h3>Redirecting....</h3></div></div>');
            setTimeout(function () {
                window.location.href = "/author";
            }, 4000);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            //    console.log(url);
            console.log(jqXHR);
            $('#result').html(jqXHR.responseText);
            console.log(textStatus);
            console.log(errorThrown);
        }
    });
});

$("#cancelToBookList").click(function(e){
    e.preventDefault();
    window.location.href = '../../';
});

$("#cancelToAuthor").click(function(e){
    e.preventDefault();
    window.location.href = '../../';
});