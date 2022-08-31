function AlertDev() {
    alert_blackout_st =
        `position: fixed;
        width: 100%;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;`

    alert_t_st =
        `padding: 25px;
        background-color: white;
        height: 200px;
        width: 300px;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;`


    alert_p_st =
        `padding-bottom: 20px;
        font-size: 16px;
        font-weight: 600;
        line-height: 110%;`

    alert_footer_st = `text-align: center;`

    alert_close_st =
        `background-color: #e8aa31;
        border-radius: 5px;
        border: none;
        padding: 8px 20px;
        color: white;
        font-weight: 600;
        cursor: pointer;`


    html =
        `<div class='alert_blackout' style='${alert_blackout_st}'>
            <div class='alert_t' style='${alert_t_st}'>
                <div class='alert_header'>        
                    <p class='alert_p' style='${alert_p_st}'>Сайт находится в стадии разработки, часть функционала недоступна.</p>
                    <p class='alert_p' style='${alert_p_st}'>Приносим свои извинения!</p>
                </div>
                <div class='alert_footer' style='${alert_footer_st}'>
                    <button type="button" class='alert_close' style='${alert_close_st}'>OK</button>
                </div> 
            </div>
        </div>`

    obj = document.querySelector('body')
    obj.setAttribute('style', 'overflow-y: hidden;')
    obj.insertAdjacentHTML('afterbegin', html)
    attr_close = document.querySelector('.alert_close')
    attr_close.addEventListener('click', AlertDevClose)
}

function AlertDevClose(e) {
    _v = e.target.closest('.alert_blackout').remove()
    obj = document.querySelector('body').removeAttribute('style')
}


function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie() {
    let date = new Date(Date.now() + 3600000000);
    date = date.toUTCString();
    document.cookie = "AlertDev=OK; expires=" + date;
}


let _getCookie = getCookie('AlertDev')
if (_getCookie != 'OK') {
    setTimeout(AlertDev, 1000)
    setCookie()
}