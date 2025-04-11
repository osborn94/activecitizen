
$(document).ready(function (){
    $('#loginward').submit(function (event) {
        event.preventDefault();

        const $entireform = $(this)
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();


        $.ajax({
            type:'POST',
            url: '/login/',
            datatype: 'json',
            data: $entireform.serialize(),
            headers:{
                'X-CSRFTOKEN':csrftoken
            },
            
            success: function(res){

                if (res.redirect_url) {
                    window.location.href = res.redirect_url;  // Redirect immediately
                }


                iziToast.success({
                    title: 'Success',
                    message: res.message || 'Logged in successfully!',
                    position: 'topLeft'
                });
                   
                // setTimeout(function () {
                //     window.location = res.redirect_url || '/';
                // }, 2000);
        

            },

            error: function(res) {
                let errorMsg = 'Something went wrong';
                if (res.responseJSON && res.responseJSON.error) {
                    errorMsg = res.responseJSON.error;
                } else if (res.status === 403) {
                    errorMsg = "Session expired. Please refresh the page and try again.";
                }
                iziToast.error({ title: 'Error', message: errorMsg });
            }

        })
    })
})