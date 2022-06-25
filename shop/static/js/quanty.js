const quantity = () => {
    const obj_quantity = document.querySelectorAll('[data-quantity]');
    for (obj_q of obj_quantity) {
        btn_all = obj_q.querySelectorAll("[data-q")
        for (let btn of btn_all) {
            btn.addEventListener('click', { handleEvent: action, 'obj_q': obj_q })
        }
    }

    function action(e) {
        const _target = e.currentTarget
        const obj = this.obj_q.querySelector('input')
        let value = parseInt(obj.value)

        if (_target.dataset.q == '+') {
            value += 1;
        } else if (_target.dataset.q == '-') {
            value -= 1
            if (value < 1) {
                value = 1
            }
        }
        obj.value = value
    }
}

quantity()




