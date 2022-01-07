var data

document.querySelector('#category-validators-id').addEventListener('change', write_form);

document.addEventListener('click', function(e) {
   let obj = e.target
   if (obj.className == 'list-group-item list-group-item-action') {
      alert_123(obj)
      feature_123(obj)
   }
});
document.addEventListener('input', function(e) {
   let obj = e.target
   if (obj.id == 'search-text') {
      search_text(obj)
   }
});

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

function html_designer2(p_obj, p_elem, p_class,p_setAtt, p_text) {
   let elem_div = document.createElement(p_elem)
   if (p_text != null) {
      elem_div.innerHTML = p_text
   }
   if (p_setAtt !=null){
      for (let i234 in p_setAtt){
         // console.log(p_setAtt)
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
   elem_html.selected=''
   elem_html.innerText = '---'
   op_obj.appendChild(elem_html)

   for (let value in p_values){
      elem_html = document.createElement('option')
      elem_html.value=value
      elem_html.innerText = p_values[value]
      op_obj.appendChild(elem_html)    
   }
}


function feature_123(obj) {
   let obj2, obj3
   let elem = document.querySelector('#product-features-update-list')

   obj1 = html_designer(elem, 'div', ['row'])
   obj2 = html_designer(obj1, 'div', ['spec', 'col-12'])
   obj3 = html_designer(obj2, 'h4', ['text-center'], 'Характеристика')
   // obj2 = html_designer(obj1, 'div', ['spec', 'col-6'])
   // obj3 = html_designer(obj2, 'h4', ['text-center'], 'Текущее значение')
   // obj2 = html_designer(obj1, 'div', ['col-md-4'])
   // obj3 = html_designer(obj2, 'h4', ['text-center'], 'Новое значение')

   get_params = '?product=' + obj.innerText
   url = "/spec/show-product-features-for-update/" + get_params
   sending_server(url)
      .then(function() {
         feature_write(data)
         // console.log('готово')
      })
}

function feature_write(data) {
   let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-nut" viewBox="0 0 16 16">
  <path d="m11.42 2 3.428 6-3.428 6H4.58L1.152 8 4.58 2h6.84zM4.58 1a1 1 0 0 0-.868.504l-3.428 6a1 1 0 0 0 0 .992l3.428 6A1 1 0 0 0 4.58 15h6.84a1 1 0 0 0 .868-.504l3.429-6a1 1 0 0 0 0-.992l-3.429-6A1 1 0 0 0 11.42 1H4.58z"/>
  <path d="M6.848 5.933a2.5 2.5 0 1 0 2.5 4.33 2.5 2.5 0 0 0-2.5-4.33zm-1.78 3.915a3.5 3.5 0 1 1 6.061-3.5 3.5 3.5 0 0 1-6.062 3.5z"/>
</svg>`
   
   let elem = document.querySelector('#product-features-update-list')
   for (elem_i in data['result']) {
      let elem2 = elem.querySelectorAll('.spec')
      row_div = html_designer(elem2[0], 'div', ['m-3','row',])
      
      attib = [['data-bs-toggle','modal'],['data-bs-target','#exampleModal']]

      html_designer2(row_div, 'button', ['btn','btn-primary', 'col-1','mb-1'],attib, svg)
      html_designer(row_div, 'div', ['col-11', 'col-md-4','mb-1'], elem_i)
      
      html_designer2(row_div, 'button', ['btn','btn-primary', 'col-1','mb-1'],attib, svg)
      html_designer(row_div, 'div', ['col-11','col-md-4','mb-1'], data['result'][elem_i])
      // html_select_list(elem2[1], data['result'][elem_i], ['form-select','m-3'])


      // html_designer(elem2[1], 'div', ['feature-name'], elem_i)
      // console.log(data['result'][elem_i])
      
   }

}

function write_form() {
   let obj_elem = document.querySelector('#category-validators-id')
   let name_input = obj_elem.options[obj_elem.selectedIndex].innerText
   let id_input = obj_elem.options[obj_elem.selectedIndex].value
   let obj_dom = document.querySelector('.product-search-ajax');
   if (obj_dom.style.display == "none") {
      obj_dom.style.display = "";
   }
};

function search_text(obj) {
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
      id_pr = data['result'][key]['id'] // option_value += `<option value="${key}">${key}</option>`;

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



// ------------------------------------------------------------------
// Основной код 
// ------------------------------------------------------------------

$(document).on('click', '#save-updated-features', function() {
   let featureNames = [];
   let featureCurrentValues = [];
   let newFeatureValues = []

   $('.feature-name').children('input').each(function() {
      featureNames.push(this.value); // "this" is the current element in the loop
   })

   $('.feature-current-value').children('input').each(function() {
      featureCurrentValues.push(this.value)
   })
   console.log($("#product-category-features-id option:selected").text())
   $('select[name="feature-value"] option:selected').each(function() {
      newFeatureValues.push(this.text)
   })

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
   let csrftoken = getCookie('csrftoken');
   let data = {
      features_names: featureNames,
      features_current_values: featureCurrentValues,
      new_feature_values: newFeatureValues,
      product: $(".product").text(),
      csrfmiddlewaretoken: csrftoken
   }
   $.ajaxSetup({
      traditional: true
   });
   $.ajax({
      method: "POST",
      data: data,
      url: '/product-specs/update-product-features-ajax/',
      success: function(data) {
         window.location.href = '/product-specs'
      }
   })
})

function removeProduct() {
   $(".search-results").css('display', 'block')
   $(".product-search-ajax").css('display', 'block')
   $(".product-features-update-list").empty()
}

function getProduct(productId, name) {
   // $(".product-features-update-list").css('display', 'block')

   $(".search-results").css('display', 'none')
   // $("#search-product-results").empty()
   // $(".product-search-ajax").css('display', 'none')
   $(".product-feature-choices").css('display', 'block')
   $(".product-feature-choices-values").css('display', 'block')
   $('input[name="search-text"]').val("")
   let data = {
      product_id: productId
   }
   $.ajax({
      method: "GET",
      data: data,
      dataType: "json",
      url: "/product-specs/show-product-features-for-update/",
      success: function(data) {
         $(".product-features-update-list").append(
            data.result
         )
      }
   })
}