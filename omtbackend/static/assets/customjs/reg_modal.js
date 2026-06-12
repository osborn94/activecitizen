$(document).on('submit', '#registrationForm', function (e) {
    e.preventDefault();

    var form = $(this);
    var formData = new FormData(this);
    const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'X-CSRFToken': csrftoken
        },
        beforeSend: function () {
            $('#btn-text').hide();
            $('.spinner-border').show();
        },
        success: function (data) {
            if (data.success) {
                iziToast.success({ title: 'Success', message: data.success });
                $('#registrationModal').modal('hide');
                // Optional: reload members list
            } else {
                iziToast.error({ title: 'Error', message: data.error || 'Something went wrong.' });
            }
        },
        error: function () {
            iziToast.error({ title: 'Error', message: 'Server error occurred.' });
        },
        complete: function () {
            $('#btn-text').show();
            $('.spinner-border').hide();
        }
    });
});
