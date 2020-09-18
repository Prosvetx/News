const get_url = function (url) {
    return url
    }

const host = '127.0.0.1:8000'
const update_url = `http://${host}/update/`;
const valute_update = document.getElementById("values_upd")
const like = document.getElementsByClassName("lk")

//Кнопка id = 'values_upd' бновление валют
valute_update.addEventListener("click", function () {
if (valute_update.innerHTML != 'done'){
   const data = {func:'update'}
   fetch(update_url, {
       method:'POST',
       headers: {'X-CSRFToken': csrftoken},
       body:JSON.stringify(data)
   }).then(response => valute_update.innerHTML = 'done')

  }
});

//Кнопка class = 'lk' зачисление и обновление лайка
for (var i = 0; like.length>i; i++) {
    like[i].addEventListener("click", function () {
    if (this.id=='lk') {
        var data = {id: parseInt(this.value)}
        fetch('', {
            method:'POST',
            headers:{'X-CSRFToken': csrftoken},
            body:JSON.stringify(data)
        }).then(response => response.json()).then(data =>
        document.getElementById('likenumb' + this.value).innerHTML = data.current_likes
        )
        }else{alert("YOU MUST BE LOGGED")}
    })
}

//Вытаскивание csrftoken'a из Cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');