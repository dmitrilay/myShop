function RequestAjax() {
  test = "123";
  url = `/smartlombard/`;
  headers = { "Content-Type": "application/json;charset=utf-8" };
  token = "6e7ed59a3894eb70fc29c2599557659215ca73ff";

  let user = {
    name: "John",
    surname: "Smith",
  };

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: JSON.stringify(_json),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      //   RenderProductSearch(data);
    })
    .catch((error) => console.log("Ошибка"));
}

_json = [
  {
    type: "add",
    data: {
      workplace: 1,
      city: "Москва",
      name: "Тестовый ломбард",
      address: "Тестовый адрес",
      phone: "Тестовый телефон",
      image: [],
      description: "Описание работы филиала",
    },
  },
  {
    type: "edit",
    data: {
      workplace: 1,
      city: "Москва",
      name: "Тестовый ломбард",
      address: "Тестовый адрес",
      phone: "Тестовый телефон",
      image: {
        src: "https://...",
        preview: "https://...",
      },
      description: "",
    },
  },
  {
    type: "remove",
    data: {
      workplace: 1,
    },
  },
];

RequestAjax();
