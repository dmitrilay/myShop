// const slider = document.getElementById('slider-handles');

// if (slider) {
//     max = 10000
//     _padding = max * 0.06
//     _max = max + _padding
//     _min = _padding * (-1)
//     noUiSlider.create(slider, {
//         start: [0, 8000],
//         connect: true,
//         padding: [_padding, _padding],
//         range: {
//             'min': [_min],
//             'max': [_max]
//         }
//     });

//     const input0 = document.getElementById('input-0');
//     const input1 = document.getElementById('input-1');
//     const inputs = [input0, input1]

//     slider.noUiSlider.on('update', f = (values, handle) => {
//         inputs[handle].value = Math.round(values[handle])
//     })

//     const setRangeSlider = (i, value) => {
//         let arr = [null, null];
//         arr[i] = value;
//         slider.noUiSlider.set(arr)
//     }

//     inputs.forEach((obj, index) => {
//         obj.addEventListener('change', (e) => {
//             setRangeSlider(index, e.currentTarget.value);
//         })
//     })

// }



const sliderUI = (slider_p) => {

    const activation = (obj) => {
        max = 10000
        _padding = max * 0.06
        _max = max + _padding
        _min = _padding * (-1)

        noUiSlider.create(obj, {
            start: [0, 8000],
            connect: true,
            padding: [_padding, _padding],
            range: {
                'min': [_min],
                'max': [_max]
            }
        });

        const body = obj.closest('.bodyUI');
        const input0 = body.querySelector('.input-0');
        const input1 = body.querySelector('.input-1');
        const inputs = [input0, input1]

        obj.noUiSlider.on('update', f = (values, handle) => {
            inputs[handle].value = Math.round(values[handle])
        })

        const setRangeSlider = (i, value) => {
            let arr = [null, null];
            arr[i] = value;
            obj.noUiSlider.set(arr)
        }

        inputs.forEach((obj, index) => {
            obj.addEventListener('change', (e) => {
                setRangeSlider(index, e.currentTarget.value);
            })
        })
    }



    for (i of slider_p) {
        activation(i)
    }
}

const _p = document.querySelectorAll('.slider-handles');
sliderUI(_p)