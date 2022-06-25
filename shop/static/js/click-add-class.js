const clickAddClass = (element) => {
    const init = () => { // Инициализация
        const spollersArray = document.querySelectorAll('[data-addclass]');
        for (i of spollersArray) {
            _setupListeners(i)
        }
    };

    const _setupListeners = (obj) => { // Добавим к элементу обработчик события
        obj.addEventListener('click', _actionClick);
    };

    const _actionClick = (e) => {
        e.preventDefault();
        const _p = e.target.dataset.addclass.split('>')
        const _class = _p[0]
        const obj = document.querySelector('.' + _p[1])
        obj.classList.add(_class)


        if (e.target.dataset.addclass2) {
            const _p2 = e.target.dataset.addclass2.split('>')
            const _class = _p2[0]
            const obj = querySel(_p2, _class)
            obj.classList.add(_class)
        }

        function querySel(_i, _class) {
            let obj = document.querySelector('.' + _i[1])
            if (obj) {
                return obj
            }
            obj = document.querySelector('#' + _i[1])
            if (obj) {
                return obj
            }
            obj = document.querySelector(_i[1])
            if (obj) {
                return obj
            }

        }
    }
    init()
}

clickAddClass('.click')