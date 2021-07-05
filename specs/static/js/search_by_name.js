// Поиск значения по имени товара
$('input[name="search-text"]').on('input', function(){
    if(this.value.length == 0){
        $(".search-results").css('display', 'none')
    } else {
        $(".search-results").css('display', 'block')
    }

    // $("#search-product-results").empty()

    let data = {
        query: this.value,
        category_id: $('select[name="category-validators"] option').filter(':selected').val()
    }

    $.ajax({
    method: "GET",
    dataType: "json",
    data: data,
    url: "/product-specs/search-product/",
    success: function(data){
        let items = []

        if(data.result.length < 1){
            $('#no-results').css('display', 'block')
        }else{
            $('#no-results').css('display', 'none')
        }
        $.each(data, function (index, value) {
            $.each(value, function (idx, v){
                if($.inArray(v, items) == -1){
                    items.push(v)
                    $('#search-product-results').append(
                        '<li class="list-group-item list-group-item-action" ' +
                        'onclick="getProduct(\'' + v.id + '\', \'' + v.name + '\')" ' +
                        'style="cursor: pointer" id="product-' +
                        v.id + '">'
                        + v.name +
                        ' | ' +
                        v.price +
                        ' руб.' +
                        '</li>')
                        }
                    })
                })
            }
        })
    })