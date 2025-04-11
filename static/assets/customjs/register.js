$(document).ready(function () {

    $('#ward-form').on('submit', function(event) {
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

        const $entireform = $(this);
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            type: 'POST',
            url: '/register/',
            dataType: 'json',
            data: $entireform.serialize(),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(res) {
                console.log('registered successfully');
                
                // Show success toast
                iziToast.success({
                    title: 'Success',
                    message: res.success || 'Account created successfully!',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true,
                    onClosing: function() {
                        // Redirect after toast closes
                        window.location = '/register';
                    }
                });
                
                // Reset form if you don't want to redirect
                // $entireform[0].reset();
                
                // Reset button state if you don't redirect
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

                // Show error toast with better configuration
                iziToast.error({
                    title: 'Error',
                    message: res.responseJSON ? res.responseJSON.error : 'An error occurred during registration.',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true
                });
            },
        });
    });


    // for local admin
    $('#local-form').on('submit', function(event) {
        event.preventDefault();
        
        const $btntext = $('#btn-text');
        const $spinner = $('.spinner-border');
        const $btnward = $('#btn-local');
        $btntext.text('Loading...');
        $spinner.show();
        $btnward.prop('disabled', true).css({
            'background-color': 'rgba(145, 113, 242, 0.83)',
            'cursor': 'not-allowed'
        });

        const $entireform = $(this);
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            type: 'POST',
            url: '/register/',
            dataType: 'json',
            data: $entireform.serialize(),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(res) {
                console.log('registered successfully');
                
                // Show success toast
                iziToast.success({
                    title: 'Success',
                    message: res.success || 'Account created successfully!',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true,
                    onClosing: function() {
                        // Redirect after toast closes
                        window.location = '/register';
                    }
                });
                
                // Reset form if you don't want to redirect
                // $entireform[0].reset();
                
                // Reset button state if you don't redirect
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

                // Show error toast with better configuration
                iziToast.error({
                    title: 'Error',
                    message: res.responseJSON ? res.responseJSON.error : 'An error occurred during registration.',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true
                });
            },
        });
    });


    // for state admin
    $('#state-form').on('submit', function(event) {
        event.preventDefault();
        
        const $btntext = $('#btn-text');
        const $spinner = $('.spinner-border');
        const $btnward = $('#btn-state');
        $btntext.text('Loading...');
        $spinner.show();
        $btnward.prop('disabled', true).css({
            'background-color': 'rgba(145, 113, 242, 0.83)',
            'cursor': 'not-allowed'
        });

        const $entireform = $(this);
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            type: 'POST',
            url: '/register/',
            dataType: 'json',
            data: $entireform.serialize(),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(res) {
                console.log('registered successfully');
                
                // Show success toast
                iziToast.success({
                    title: 'Success',
                    message: res.success || 'Account created successfully!',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true,
                    onClosing: function() {
                        // Redirect after toast closes
                        window.location = '/register';
                    }
                });
                
                // Reset form if you don't want to redirect
                // $entireform[0].reset();
                
                // Reset button state if you don't redirect
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

                // Show error toast with better configuration
                iziToast.error({
                    title: 'Error',
                    message: res.responseJSON ? res.responseJSON.error : 'An error occurred during registration.',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true
                });
            },
        });
    });


    // for national admin
    $('#national-form').on('submit', function(event) {
        event.preventDefault();
        
        const $btntext = $('#btn-text');
        const $spinner = $('.spinner-border');
        const $btnward = $('#btn-national');
        $btntext.text('Loading...');
        $spinner.show();
        $btnward.prop('disabled', true).css({
            'background-color': 'rgba(145, 113, 242, 0.83)',
            'cursor': 'not-allowed'
        });

        const $entireform = $(this);
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            type: 'POST',
            url: '/register/',
            dataType: 'json',
            data: $entireform.serialize(),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(res) {
                console.log('registered successfully');
                
                // Show success toast
                iziToast.success({
                    title: 'Success',
                    message: res.success || 'Account created successfully!',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true,
                    onClosing: function() {
                        // Redirect after toast closes
                        window.location = '/register';
                    }
                });
                
                // Reset form if you don't want to redirect
                // $entireform[0].reset();
                
                // Reset button state if you don't redirect
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

                // Show error toast with better configuration
                iziToast.error({
                    title: 'Error',
                    message: res.responseJSON ? res.responseJSON.error : 'An error occurred during registration.',
                    position: 'topCenter',
                    timeout: 5000,
                    closeOnClick: true
                });
            },
        });
    });


});
