// var data
// var id_button

var id_product
var name_product_id
var old_value_id

var list_spec
var myModal = new bootstrap.Modal(document.getElementById('exampleModal'))
var myModal_spec_del = new bootstrap.Modal(document.getElementById('exampleModal2'))

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

   // Возврат к первоначальному состаяни (выбор продукта)
   if (obj.className == 'btn-close') {
      clearing_content(obj.parentElement.className)
   }

   // Открываем модальное окно для редактирования значий характеристики
   if (obj.id == 'btn-edit') {
      editing_characteristics(obj)
   } else if (obj.parentElement.id == 'btn-edit') {
      editing_characteristics(obj.parentElement)
   }

   // Открываем модальное окно для подтверждения удаления характеристики
   if (obj.id == 'btn-del') {
      remove_characteristic(obj)
   } else if (obj.parentElement.id == 'btn-del') {
      remove_characteristic(obj.parentElement)
   }

   // Подтверждения удаления характеристики
   if (obj.id == 'click-btn-del') {
      click_remove_characteristic(obj)
   }

   // ---
   if (obj.className == 'list-group-item list-group-item-action') {
      name_product_id = obj.value
      alert_123(obj)
      feature_123(obj)
   }
   // Добавление характеристики к товару
   if (obj.getAttribute('add_spec_modal') == 'modal') {
      add_characteristics(obj)
   }
   // Сохранения нового значения для продукта
   if (obj.getAttribute('modal') == 'save-vl') {
      save_value(obj)
   } else if (obj.getAttribute('modal') == 'save-vl2') {
      save_new_value_spec()
   }
});

document.addEventListener('input', function(e) {
   let obj = e.target
   if (obj.id == 'search-text') {
      search_text(obj)
   }
});


function clearing_content(obj) {
   document.querySelector('#product-features-update-list').innerHTML = ''
   document.querySelector('.product').innerHTML = ''
   document.querySelector('#search-text').value = ''

   document.querySelector('.category-validator-div').style.display = ''
   document.querySelector('.product-search-ajax').style.display = ''
   document.querySelector('.product').style.display = ''
}

function click_remove_characteristic(obj) {
   myModal_spec_del.hide();
   let elem = document.querySelector('#del-value')
   let id_characteristic = elem.getAttribute('value')
   get_params = `?purpose=6&id_characteristic=${id_characteristic}&id_product=${name_product_id}`
   url = "/spec/show-product-features-for-update" + get_params
   sending_server(url).then(function() {
      obj2 = document.querySelector('#product-features-update-list')
      obj2.innerHTML = ''
      setTimeout(feature_123, 500, id_product);
   })
}

function remove_characteristic(obj) {
   myModal_spec_del.show();
   let data = list_spec
   for (i in data['result']) {
      if (data['result'][i][0] == obj.value) {
         let elem = document.querySelector('#del-value')
         elem.innerText = `${i} // ${data['result'][i][1]}`
         elem.setAttribute('value', data['result'][i][0])
      }
   }
}

function save_new_value_spec(obj) {
   myModal.hide();

   let name_characteristic = document.querySelector('#value-spec-validators').value
   let name_value = document.querySelector('#value-spec-select-validators').value
   let product = name_product_id

   get_params = `?purpose=5&name_characteristic=${name_characteristic}&name_value=${name_value}&product=${product}`
   url = "/spec/show-product-features-for-update" + get_params
   sending_server(url).then(function() {
      obj2 = document.querySelector('#product-features-update-list')
      obj2.innerHTML = ''
      setTimeout(feature_123, 500, id_product);
   })
}

function save_value(obj) {
   myModal.hide();
   new_value_name = document.querySelector('#select-value')
   get_params = `?purpose=2&value_id=${old_value_id}&new_value_name=${new_value_name.value}`
   url = "/spec/show-product-features-for-update" + get_params
   sending_server(url).then(function() {
      obj2 = document.querySelector('#product-features-update-list')
      obj2.innerHTML = ''
      setTimeout(feature_123, 500, id_product);
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

   old_value_id = id_product.value
   get_params = `?purpose=3&value_id=${old_value_id}`
   url = "/spec/show-product-features-for-update" + get_params

   sending_server(url).then(function() {
      myModal.show();
      let elem = document.querySelector('#modal-1')
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
   myModal.show()
   let elem = document.querySelector('#modal-1')
   elem.innerHTML = ''
   html_designer(elem, 'label', [], 'Текущие значение')
   let elem1 = html_designer(elem, 'div', ['form-control', 'mb-2'], 'Идет загрузка...')
   elem1.id = 'current-value'
   html_designer(elem, 'label', [], 'Новое значение')
   attib = [
      ['id', 'select-value'],
      ['aria-label', 'Default select example'],
   ]
   let elem2 = html_designer2(elem, 'select', ['form-select', ], attib, '')
   document.querySelector('#save').setAttribute('modal', 'save-vl')

   old_value_id = obj.value
   get_params = `?purpose=1&value_id=${obj.value}`
   url = "/spec/show-product-features-for-update" + get_params

   sending_server(url).then(function() {
      elem1.innerText = data['result'][1]
      attib = [
         ['selected', ''],
      ]
      html_designer2(elem2, 'option', [], attib, '---')
      for (let i in data['result'][0]) {
         p = data['result'][0][i]
         attib = [
            ['value', p],
         ]
         html_designer2(elem2, 'option', [], attib, p)
      }
   })
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
         list_spec = data
         feature_write(data)
      })
}

function feature_write(data) {
   let elem = document.querySelector('#product-features-update-list')
   let elem2 = elem.querySelectorAll('.spec')

   for (elem_i in data['result']) {
      row_div = html_designer(elem2[0], 'div', ['mb-2', 'row', 'border', 'rounded', 'col-12', 'col-lg-6'])
      attib = [
         ['value', data['result'][elem_i][0]],
         ['id', 'btn-del'],
      ]
      html_designer2(row_div, 'button', ['btn', 'btn-danger', 'btn-sm', 'col-1', 'm-1', ], attib, '<i class="fa fa-trash"></i>')
      attib = [
         ['id', 'btn-edit'],
         ['value', data['result'][elem_i][0]],
      ]
      html_designer2(row_div, 'button', ['btn', 'btn-primary', 'btn-sm', 'col-1', 'm-1'], attib, '<i class="fa fa-edit"></i>')
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

   attib = [
      ['id', 'product-title'],
   ]
   myElement = html_designer2(myElement, 'div', ['alert', 'alert-info', 'alert-dismissible', 'show'], attib, obj.innerText)

   html_designer2(myElement, 'button', ['btn-close'], [], [])
   remove_search_text()

   document.querySelector('.category-validator-div').style.display = 'none' // скрыть строку поиска
   document.querySelector('.product-search-ajax').style.display = 'none' // скрыть строку поиска
};

// ============================================
// функции для построения HTML
// ============================================
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