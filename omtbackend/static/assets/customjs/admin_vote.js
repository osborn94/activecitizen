$(document).ready(function () {
    $('#wardForm').submit(function (event) {
        event.preventDefault();

        const $form = $(this);
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        const $btnward = $form.find('#btn-ward');
        const $btntext = $form.find('#btn-text');
        const $spinner = $form.find('.spinner-border');

        function resetButton() {
            $btntext.text('Vote');
            $spinner.hide();
            $btnward.prop('disabled', false).css({
                'background-color': '',
                'cursor': 'pointer'
            });
        }

        // Set loading state
        $btntext.text('Submitting...');
        $spinner.show();
        $btnward.prop('disabled', true).css({
            'background-color': 'rgba(145, 113, 242, 0.83)',
            'cursor': 'not-allowed'
        });

        $.ajax({
            type: 'POST',
            url: $form.attr('action') || '/next-step/',  // in case you ever change the URL
            data: $form.serialize(),
            headers: {
                'X-CSRFTOKEN': csrftoken
            },
            dataType: 'json',

            success: function (res) {
                console.log("Response:", res);

                if (res.success) {
                    iziToast.success({
                        title: 'Success',
                        message: res.message || 'Nomination recorded successfully!',
                        position: 'topCenter',
                        timeout: 1500,
                        closeOnClick: true
                    });

                    setTimeout(() => {
                        if (res.redirect_url) {
                            window.location.href = res.redirect_url;
                        } else {
                            resetButton();
                            $form.trigger('reset'); // Clear form if no redirect
                        }
                    }, 1600);
                } else {
                    iziToast.error({
                        title: 'Error',
                        message: res.error || 'Failed to submit nomination'
                    });
                    resetButton();
                }
            },

            error: function (res) {
                let errorMsg = 'Something went wrong. Please try again.';

                if (res.status === 403 && res.responseJSON?.redirect_url) {
                    iziToast.warning({
                        title: 'Verification Required',
                        message: res.responseJSON.error || 'Please verify your email.',
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
                    errorMsg = "Session expired. Please refresh the page.";
                }

                iziToast.error({ title: 'Error', message: errorMsg });
                resetButton();
            }
        });
    });
});
