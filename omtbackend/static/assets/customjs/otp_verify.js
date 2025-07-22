$(document).ready(function () {

    $('#otpForm').on('submit', function(event) {
        event.preventDefault();
        
        const $btntext = $('#btn-text');
        const $spinner = $('.spinner-border');
        const $btnward = $('#btn-ward');

        $btntext.text('Loading...');
        $spinner.show();
        $btnward.prop('disabled', true).css({
            'background-color': 'rgba(145, 113, 242, 0.83)',
            'cursor': 'not-allowed'
        });

        const formElement = this; // Native DOM element
        const formData = new FormData(formElement);
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            type: 'POST',
            url: '/verify-otp/',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(res) {
                console.log('Response:', res);

                if (res.success) {
                    iziToast.success({
                        title: 'Success',
                        message: res.message || 'Verified successfully!',
                        position: 'topCenter',
                        timeout: 5000,
                        closeOnClick: true,
                        onClosing: function() {
                            window.location = res.redirect_url || '/login';
                        }
                    });
                } else {
                    iziToast.error({
                        title: 'Error',
                        message: res.error || 'Something went wrong during verification.',
                        position: 'topCenter',
                        timeout: 5000,
                        closeOnClick: true
                    });
                }
            },
            error: function(res) {
                console.log("Error response:", res);
                console.log("Status code:", res.status);
                console.log("Response text:", res.responseText);
                console.log("Response JSON:", res.responseJSON);

                $btntext.text('Register Now');
                $spinner.hide();
                $btnward.prop('disabled', false).css({
                    'background-color': '',
                    'cursor': '',
                });

                iziToast.error({
                    title: 'Error',
                    message: res.responseJSON ? res.responseJSON.error : 'An error occurred during registration.',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true
                });
            }
        });
    });

});
