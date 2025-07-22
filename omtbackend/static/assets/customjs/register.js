$(document).ready(function () {

    $('#registrationForm').on('submit', function(event) {
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
            url: '/register/',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(res) {
                console.log('registered successfully');

                iziToast.success({
                    title: 'Success',
                    message: res.success || 'Account created successfully!',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true,
                    onClosing: function() {
                        window.location = '/verify-otp';
                    }
                });

                // Optional: Reset the form if needed
                // formElement.reset();
                // $btntext.text('Register Now');
                // $spinner.hide();
                // $btnward.prop('disabled', false).css({
                //     'background-color': '',
                //     'cursor': ''
                // });
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
