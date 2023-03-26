let form_fields = document.getElementsByTagName("input");
form_fields[1].placeholder = "Введите логин";
form_fields[2].placeholder = "Введите имя";
form_fields[3].placeholder = "Введите почту";
form_fields[4].placeholder = "Введите пароль";
form_fields[5].placeholder = "Повтор пароля";

for (let field in form_fields) {
    form_fields[field].className += " form-control";
}