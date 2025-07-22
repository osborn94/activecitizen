$(document).ready(function () {
    $('#loginForm').submit(function (event) {
        event.preventDefault();

        const $form = $(this);
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        // Get button elements inside the form
        const $btnward = $form.find('#btn-ward');
        const $btntext = $form.find('#btn-text');
        const $spinner = $form.find('.spinner-border');

        function resetButton() {
            $btntext.text('Login');
            $spinner.hide();
            $btnward.prop('disabled', false).css({
                'background-color': '',
                'cursor': 'pointer'
            });
        }

        // Show loading
        $btntext.text('Loading...');
        $spinner.show();
        $btnward.prop('disabled', true).css({
            'background-color': 'rgba(145, 113, 242, 0.83)',
            'cursor': 'not-allowed'
        });

        $.ajax({
            type: 'POST',
            url: '/login/',
            dataType: 'json',
            data: $form.serialize(),
            headers: {
                'X-CSRFTOKEN': csrftoken
            },
            xhrFields: {
                withCredentials: true
            },

            success: function (res) {
                console.log("Response:", res);
                console.log("Redirect URL:", res.redirect_url);
                console.log("Document cookies:", document.cookie);

                if (res.success) {
                    iziToast.success({
                        title: 'Success',
                        message: res.message || 'Logged in successfully!',
                        position: 'topCenter',
                        timeout: 1500,
                        closeOnClick: true
                    });

                    setTimeout(() => {
                        window.location.href = res.redirect_url || '/';
                    }, 1600);
                } else {
                    iziToast.error({
                        title: 'Error',
                        message: res.error || 'Login failed. Please try again.'
                    });
                    resetButton(); //  Now this works perfectly
                }
            },

            error: function (res) {
                let errorMsg = 'Something went wrong';

                if (res.status === 403 && res.responseJSON?.redirect_url) {
                    iziToast.warning({
                        title: 'Email Not Verified',
                        message: res.responseJSON.error || 'Verification required.',
                        timeout: 1500,
                        position: 'topCenter',
                        closeOnClick: true
                    });

                    setTimeout(() => {
                        window.location.href = res.responseJSON.redirect_url;
                    }, 1700);

                    return;
                }

                if (res.responseJSON?.error) {
                    errorMsg = res.responseJSON.error;
                } else if (res.status === 403) {
                    errorMsg = "Session expired. Please refresh the page and try again.";
                }

                iziToast.error({ title: 'Error', message: errorMsg });
                resetButton(); //  Button and spinner reset even on AJAX error
            }
        });
    });
});
