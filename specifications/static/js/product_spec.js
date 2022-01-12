var data
var id_button
var id_product
var name_product_id
var old_value_id
var myModal = new bootstrap.Modal(document.getElementById('exampleModal'))

document.addEventListener('change', function(e) {
   let obj = e.target
   if (obj.id == 'category-validators-id') {
      write_form(obj)
   } else if (obj.id == 'value-spec-validators') {
      add_characteristics_value(obj)
   }

})
document.addEventListener('click', function(e) {
   let obj = e.target
   if (obj.className == 'list-group-item list-group-item-action') {
      name_product_id = obj.value
      alert_123(obj)
      feature_123(obj)
   }
   // if (obj.getAttribute('att_bootstrap') == 'modal') {
   //    editing_characteristics(obj)
   // }

   // Добавление характеристики к товару
   if (obj.getAttribute('add_spec_modal') == 'modal') {
      add_characteristics(obj)
   }

   // console.log(obj)
   // Удаление характеристики из товара
   // if (obj.getAttribute('fill') == 'currentColor') {
   //    console.log(obj.children)
   //    // editing_characteristics(obj.parentElement)
   //    // alert('удаление')
   // }

   if (obj.getAttribute('modal') == 'save-vl') {
      save_value(obj)
   } else if (obj.getAttribute('modal') == 'save-vl2') {
      save_new_value_spec()
   }


   let btn_del = document.querySelector('#btn-del')
   if (btn_del.contains(obj)) {
      alert('удалить2')
   }
   let btn_edit = document.querySelector('#btn-edit')
   if (btn_edit.contains(obj)) {
      editing_characteristics(obj)
   }

});
document.addEventListener('input', function(e) {
   let obj = e.target
   if (obj.id == 'search-text') {
      search_text(obj)
   }
});

function save_new_value_spec(obj) {
   myModal.hide();
   // obj2 = document.querySelector('#product-features-update-list')
   // obj2.innerHTML = ''

   let name_characteristic = document.querySelector('#value-spec-validators').value
   let name_value = document.querySelector('#value-spec-select-validators').value
   let product = name_product_id

   get_params = `?purpose=5&name_characteristic=${name_characteristic}&name_value=${name_value}&product=${product}`
   url = "/spec/show-product-features-for-update" + get_params
   sending_server(url).then(function() {
      // setTimeout(feature_123, 1000, id_product);
      console.log('успех')
   })
}

function save_value(obj) {
   myModal.hide();
   obj2 = document.querySelector('#product-features-update-list')
   obj2.innerHTML = ''

   new_value_name = document.querySelector('#select-value')
   get_params = `?purpose=2&value_id=${old_value_id}&new_value_name=${new_value_name.value}`
   url = "/spec/show-product-features-for-update" + get_params
   sending_server(url).then(function() {
      setTimeout(feature_123, 1000, id_product);
   })
}

function add_characteristics_value(obj) {
   get_params = `?purpose=4&value_id=${obj.value}`
   url = "/spec/show-product-features-for-update" + get_params
   sending_server(url).then(function() {

      attib = [
         ['aria-label', 'Default select example'],
         ['id', 'value-spec-select-validators'],
      ]
      let elem = document.querySelector('.modal-body')
      let elem2 = document.querySelector('#value-spec-select-validators')
      if (elem2 == null) {
         elem_select = html_designer2(elem, 'select', ['form-select', 'mt-3'], attib, [])
      } else {
         elem2.innerHTML = ''
      }

      attib = [
         ['aria-label', 'Default select example'],
         ['class', 'form-select'],
         ['id', 'value-spec-validators']
      ]

      html_designer2(elem_select, 'option', [], attib, '---')
      for (let i in data['result']) {
         p = data['result'][i]
         attib = [
            ['value', i],
         ]
         html_designer2(elem_select, 'option', [], attib, p)
      }

   })
}

function add_characteristics(obj) {
   document.querySelector('#save').setAttribute('modal', 'save-vl2')


   // .getAttribute('modal') = 'save-vl2'
   old_value_id = id_product.value
   get_params = `?purpose=3&value_id=${old_value_id}`
   url = "/spec/show-product-features-for-update" + get_params

   sending_server(url).then(function() {
      myModal.show();
      let elem = document.querySelector('.modal-body')
      elem.innerHTML = ''
      attib = [
         ['aria-label', 'Default select example'],
         ['class', 'form-select'],
         ['id', 'value-spec-validators']
      ]
      elem_select = html_designer2(elem, 'select', [], attib, [])
      html_designer2(elem_select, 'option', [], attib, '---')
      for (let i in data['result']) {
         p = data['result'][i]
         attib = [
            ['value', i],
         ]
         html_designer2(elem_select, 'option', [], attib, p)
      }

   })
}

function editing_characteristics(obj) {
   // ручной запуск модального окна bootstrap
   myModal.show();
   document.querySelector('#save').setAttribute('modal', 'save-vl')
   old_value_id = obj.value
   get_params = `?purpose=1&value_id=${obj.value}`
   url = "/spec/show-product-features-for-update" + get_params

   sending_server(url).then(function() {
      let elem = document.querySelector('#current-value')
      elem.innerText = data['result'][1]

      elem = document.querySelector('#select-value')
      elem.innerHTML = ''
      attib = [
         ['selected', ''],
      ]
      html_designer2(elem, 'option', [], attib, '---')
      for (let i in data['result'][0]) {
         p = data['result'][0][i]
         // console.log(p)
         attib = [
            ['value', p],
         ]
         html_designer2(elem, 'option', [], attib, p)
      }


      // alert(data)
      // test(data)
   })
}

function html_designer(p_obj, p_elem, p_class, p_text) {
   let elem_div = document.createElement(p_elem)
   if (p_text != null) {
      elem_div.innerText = p_text
   }

   for (i in p_class) {
      elem_div.classList.add(p_class[i])
   }
   return p_obj.appendChild(elem_div)
}

function html_designer2(p_obj, p_elem, p_class, p_setAtt, p_text) {
   let elem_div = document.createElement(p_elem)
   if (p_text != null) {
      elem_div.innerHTML = p_text
   }
   if (p_setAtt != null) {
      for (let i234 in p_setAtt) {
         elem_div.setAttribute(p_setAtt[i234][0], p_setAtt[i234][1])
      }
   }

   for (i in p_class) {
      elem_div.classList.add(p_class[i])
   }
   return p_obj.appendChild(elem_div)
}

function html_select_list(p_obj, p_values, p_class, p_text) {
   let elem_div = document.createElement('select')
   if (p_text != null) {
      elem_div.innerText = p_text
   }

   for (i in p_class) {
      elem_div.classList.add(p_class[i])
   }

   op_obj = p_obj.appendChild(elem_div)
   let = elem_html = document.createElement('option')
   elem_html.selected = ''
   elem_html.innerText = '---'
   op_obj.appendChild(elem_html)

   for (let value in p_values) {
      elem_html = document.createElement('option')
      elem_html.value = value
      elem_html.innerText = p_values[value]
      op_obj.appendChild(elem_html)
   }
}

function feature_123(obj) {
   id_product = obj
   let obj2, obj3
   let elem = document.querySelector('#product-features-update-list')

   obj1 = html_designer(elem, 'div', ['row'])
   obj2 = html_designer(obj1, 'div', ['spec', 'col-12'])
   obj3 = html_designer(obj2, 'h4', ['text-center'], 'Характеристика')

   get_params = '?product=' + obj.innerText
   url = "/spec/show-product-features-for-update/" + get_params
   sending_server(url)
      .then(function() {
         feature_write(data)
      })
}

function feature_write(data) {
   let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-nut" viewBox="0 0 16 16">
  <path d="m11.42 2 3.428 6-3.428 6H4.58L1.152 8 4.58 2h6.84zM4.58 1a1 1 0 0 0-.868.504l-3.428 6a1 1 0 0 0 0 .992l3.428 6A1 1 0 0 0 4.58 15h6.84a1 1 0 0 0 .868-.504l3.429-6a1 1 0 0 0 0-.992l-3.429-6A1 1 0 0 0 11.42 1H4.58z"/>
  <path d="M6.848 5.933a2.5 2.5 0 1 0 2.5 4.33 2.5 2.5 0 0 0-2.5-4.33zm-1.78 3.915a3.5 3.5 0 1 1 6.061-3.5 3.5 3.5 0 0 1-6.062 3.5z"/></svg>`

   let elem = document.querySelector('#product-features-update-list')
   let elem2 = elem.querySelectorAll('.spec')

   for (elem_i in data['result']) {
      row_div = html_designer(elem2[0], 'div', ['mb-2', 'row', 'border', 'rounded', 'col-12', 'col-lg-6'])

      attib = [
         ['value', data['result'][elem_i][0]],
         ['id', 'btn-del'],
      ]
      html_designer2(row_div, 'button', ['btn', 'btn-danger', 'btn-sm', 'col-1', 'm-1', ], attib, svg)
      attib = [
         ['id', 'btn-edit'],
         ['value', data['result'][elem_i][0]],
      ]
      html_designer2(row_div, 'button', ['btn', 'btn-primary', 'btn-sm', 'col-1', 'm-1'], attib, svg)
      // html_designer(row_div, 'div', ['col-11', 'col-md-4', 'mb-1'], elem_i)
      name_spec_value = `${elem_i} // ${data['result'][elem_i][1]}`
      html_designer(row_div, 'div', ['col-9', 'm-0', 'text-truncate'], name_spec_value)


   }
   att_class = ['col-12', 'col-lg-6', 'btn', 'btn-outline-secondary', 'btn-lg', 'mt-6']
   att_other = [
      ['add_spec_modal', 'modal'],
      ['value', data['result'][elem_i][0]],
   ]
   html_designer2(elem2[0], 'button', att_class, att_other, '+')
}

function write_form() {
   let obj_elem = document.querySelector('#category-validators-id')
   let name_input = obj_elem.options[obj_elem.selectedIndex].innerText
   let id_input = obj_elem.options[obj_elem.selectedIndex].value
   let obj_dom = document.querySelector('.product-search-ajax');
   if (obj_dom.style.display == "none") {
      obj_dom.style.display = "";
   }
}

function search_text(obj) {
   id_product = obj.value
   category_id = document.querySelector('#category-validators-id').value
   get_params = '?query=' + obj.value + '&category_id=' + category_id
   url = "/spec/search-product/" + get_params
   let rez
   if (obj.value.length > 0) {
      remove_search_text()
   }
   if (obj.value.length > 2) {
      sending_server(url)
         .then(function() {
            test(data)
         })
   }
}

function remove_search_text() {
   let element_search_results = document.querySelector('.search-results')
   document.querySelector('#search-product-results').remove()

   let obj_ul = document.createElement('ul')
   obj_ul.classList.add('list-group')
   obj_ul.id = 'search-product-results'
   element_search_results.appendChild(obj_ul)
}

function test(data) {
   for (var key in data['result']) {
      name_pr = data['result'][key]['name']
      id_pr = data['result'][key]['id']

      let myElement = document.querySelector('#search-product-results')
      let obj_li = document.createElement('li')
      obj_li.classList.add('list-group-item')
      obj_li.classList.add('list-group-item-action')
      obj_li.textContent = name_pr
      obj_li.value = id_pr
      myElement.appendChild(obj_li)
   }
}

function sending_server(requestURL) {
   return new Promise(function(resolve, reject) {
      const xhr = new XMLHttpRequest()
      xhr.open('GET', requestURL)
      xhr.responseType = 'json'
      xhr.send()
      xhr.onload = function() {
         if (xhr.status != 200) {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
         } else {
            data = xhr.response
            resolve(data)
         }
      }
   })
}

function alert_123(obj) {
   let myElement = document.querySelector('.product')
   let obj_div = document.createElement('div')
   obj_div.classList.add('alert')
   obj_div.classList.add('alert-info')
   obj_div.classList.add('alert-dismissible')
   obj_div.classList.add('show')
   obj_div.id = "product-title"
   obj_div.setAttribute('role', 'alert')
   obj_div.innerText = obj.innerText
   myElement = myElement.appendChild(obj_div)

   let obj_elm = document.createElement('button')
   obj_elm.type = "button"
   obj_elm.classList.add('btn-close')
   obj_elm.setAttribute('data-bs-dismiss', 'alert')
   obj_elm.setAttribute('onclick', 'removeProduct()')
   myElement.appendChild(obj_elm)
   remove_search_text()
   document.querySelector('.category-validator-div').style.display = 'none' // скрыть строку поиска
   document.querySelector('.product-search-ajax').style.display = 'none' // скрыть строку поиска
};