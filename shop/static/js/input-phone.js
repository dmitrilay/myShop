document.addEventListener("DOMContentLoaded", function () {
  let phoneInput = document.querySelectorAll("input[data-tel-input]");

  let getInputNumbersValue = function (input) {
    return input.value.replace(/\D/g, "");
  };

  let onPhoneInput = function (e) {
    let input = e.target,
      inputValue = input.value;
    inputNumbersValue = getInputNumbersValue(input);
    formattedInputValue = "";
    SelectionStart = input.selectionStart;

    if (!inputNumbersValue) {
      return (input.value = "");
    }

    if (SelectionStart != 0) {
      if (input.value.length != SelectionStart) {
        if (e.data && /\D/g.test(e.data)) {
          input.value = inputNumbersValue;
        }
        return;
      }
    }

    // if (inputNumbersValue[0] == "9") inputNumbersValue = "7" + inputNumbersValue;

    // let firstSymbols = inputNumbersValue[0] == "8" ? "8" : "+7";

    if (inputNumbersValue[0] == "7") {
      inputNumbersValue[0] = "7";
    } else if (inputNumbersValue[0] == "8") {
      inputNumbersValue[0] = "8";
    } else {
      inputNumbersValue = "7" + inputNumbersValue;
    }

    firstSymbols = inputNumbersValue[0];

    formattedInputValue = firstSymbols + " ";

    if (inputNumbersValue.length > 1) {
      formattedInputValue += "(" + inputNumbersValue.substring(1, 4);
    }

    if (inputNumbersValue.length >= 5) {
      formattedInputValue += ") " + inputNumbersValue.substring(4, 7);
    }

    if (inputNumbersValue.length >= 8) {
      formattedInputValue += "-" + inputNumbersValue.substring(7, 9);
    }

    if (inputNumbersValue.length >= 10) {
      formattedInputValue += "-" + inputNumbersValue.substring(9, 11);
    }

    input.value = formattedInputValue;
  };

  let onPhoneKetDown = function (e) {
    let input = e.target;
    if (e.keyCode == 8 && getInputNumbersValue(input).length == 1) {
      input.value = "";
    }
  };

  let onPhonePaste = function (e) {
    let pasted = e.clipboardData || window.clipboardData,
      input = e.target;
    inputNumbersValue = getInputNumbersValue(input);
    if (pasted) {
      let pastedText = pasted.getData("Text");
      if (/\D/g.test(pastedText)) {
        input.value = inputNumbersValue;
      }
    }
  };

  let startInput = function (e) {
    let input = e.target;
    let inputValue = input.value;
    if (inputValue.length == 0) {
      input.value = "+7 ";
    }
  };

  for (i = 0; i < phoneInput.length; i++) {
    let input = phoneInput[i];

    input.addEventListener("click", startInput);
    input.addEventListener("input", onPhoneInput);
    input.addEventListener("keydown", onPhoneKetDown);
    input.addEventListener("paste", onPhonePaste);

    let myEvent = new Event("input");
    input.dispatchEvent(myEvent);
  }
});
