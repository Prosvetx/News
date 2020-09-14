$(document).ready(function () {

    $(".lk").click(function () {
        $.ajax({
                url: '',
                type: 'post',
                data: {
                    id: $(this).val(),
                    csrfmiddlewaretoken: csrftoken

                },
                success: function (response) {
                    let idpk = "#likenumb" + response.id;
                    $(idpk).text(response.current_likes);

                }
            }
        )
    });

    $("[id=bk]").on('click', function () {
        alert('ЗАЛОГИНЬСЯ!')
    })

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');