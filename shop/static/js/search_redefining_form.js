{
  document.addEventListener("DOMContentLoaded", search_redefining_form);

  function search_redefining_form(self) {
    const _d = document.querySelectorAll("form.filters");

    function disabling_button() {
      const _btn = _d[0].querySelector("a.buttons-filters__btn");
      if (_btn) {
        _btn.style = "display: none;";
      }
    }

    function redefining_form() {
      _d[0].addEventListener("submit", (e) => {
        e.preventDefault();
        let input = document.createElement("input");
        input.name = "qu";
        input.value = get_value_search();
        input.style = "display: none;";
        e.target.append(input);
        e.target.submit();
      });
    }

    function get_value_search() {
      let _p = location.search.replace("?", "").split("&");
      let value_search = "";
      for (item of _p) {
        if (item.slice(0, 3) == "qu=") value_search = item.slice(3);
      }
      console.log(value_search);
      return value_search;
    }
    // get_value_search();
    disabling_button();
    redefining_form();
  }
}
