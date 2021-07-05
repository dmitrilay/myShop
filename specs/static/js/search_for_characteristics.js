$('select[name="category-validators"]').on('change', function() {
    var categoryId = this.value;
    data = {
        category_id: categoryId
    }
    prev_choice = categoryId
    $(".feature-validator-div").empty()
    $(".feature-value-div").empty()
    $(".errors").empty()
    $.ajax({
        method: "GET",
        dataType: "json",
        data: data,
        url: "/product-specs/feature-choice/",
        success: function(data){
            $(".feature-validator-div").css('display', 'block');

            var option_value
            for (var key in data['result']){
                option_value += `<option value="${key}">${key}</option>`
            }

            html_select = `
            <select class="form-select" name="feature-validators" id="feature-validators-id" aria-label="Default select example">
                <option selected>---</option> ${option_value} </select>`;

            $(".feature-validator-div").append(html_select)
        }
    })
});

$(document).on('change', 'select[name="feature-validators"]', function(){
    $('.feature-value-div').empty()
    $('.errors').empty()
    $('.feature-value-div').append(
        '<input type="text" class="form-control" id="feature-value" required></input>',
        '<br>',
        '<input type="submit" class="btn btn-success" id="create-validator" value="Создать">'
    )
})