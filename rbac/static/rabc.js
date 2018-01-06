 $(function () {
    $('.item-title').click(function () {
        // if($(this).next().hasClass('hide')){
        //     $(this).next().removeClass('hide')
        // }else{
        //     $(this).next().addClass('hide')
        // }
        $(this).next().toggleClass("hide")
    })


});