$(document).ready(function () {
    $('#memForm').submit(function (event) {
        event.preventDefault();

        const $form = $(this);
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        const actionUrl = $form.attr('action');

        const $btnward = $form.find('#btn-mem');

        function resetButton() {
            $btnward.prop('disabled', false).css({
                'background-color': '',
                'cursor': 'pointer'
            });
        }

        $.ajax({
            type: 'POST',
            url: actionUrl,
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

                if (res.success) {
                    iziToast.success({
                        title: 'Success',
                        message: res.message || 'Approved successfully!',
                        position: 'topCenter',
                        timeout: 1500,
                        closeOnClick: true
                    });

                    const $modal = $form.closest('.modal');
                    $modal.modal('hide');

                    setTimeout(() => {
                        location.reload();
                    }, 1000);


                } else {
                    iziToast.error({
                        title: 'Error',
                        message: res.error || 'Not Approved. Please try again.'
                    });
                    resetButton();
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
                resetButton();
            }
        });
    });
});
